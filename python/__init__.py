import os
import sys
import imp
import pdb
import csv
import json
import uuid
import readline, rlcompleter
import time, logging, datetime
from logging.config import dictConfig
from functools import wraps
from xml.dom import minidom
from xml.etree import cElementTree as ctree
from pprint import pprint as pp

from importlib import import_module

py_version = sys.version_info[0]

if py_version > 2:
    def execfile(filename):
        with open(filename) as fd:
            code = compile(fd.read(), filename, 'exec')
            exec(code, globals(), locals())


HOME_DIR = os.environ.get('HOME')
HOME_SCRIPTS = os.environ['HOME_SCRIPTS']
HOME_SCRIPTS_PYTHON = os.path.join(HOME_SCRIPTS, 'python')

# SETTING UP DEFAULT LOGGER
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
        'syslog': {
            'level': 'DEBUG',
            'address': '/dev/log',
            'class': 'logging.handlers.SysLogHandler',
            'formatter': 'syslog',
        },
    },
    'formatters': {
        'syslog': {
            'format': '%(levelname)s %(name)s.%(funcName)s: %(message)s',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console', 'syslog'],
            'level': 'DEBUG',
            'propragate': True,
        }
    }
}

dictConfig(LOGGING)

logger = logging.getLogger('default_logger')


# AUTO COMPLETION
logger.info("SETTING UP AUTOCOMPLETION")
if 'libedit' in readline.__doc__:
    readline.parse_and_bind("bind ^I rl_complete")
else:
    readline.parse_and_bind("tab: complete")

if sys.version_info < (3.0,):
    execfile(os.path.join(HOME_SCRIPTS, 'python', 'db.py'))


# USEFUL METHOD
def get_real_path(f):
    """Retuns the realpath of a file
    """
    return os.path.realpath(f)


def get_joined_path(a, b):
    """Returns joined path of to file
    """
    return os.path.join(a, b)


def get_file_content(filename):
    """Returns content of a given file
    """
    with open(filename) as f:
        return f.read()


def write_content_into_file(content, filename):
    """Save content into the given file
    """
    with open(filename, 'wb') as fd:
        fd.write(content)


# MY DECORATORS
def timethis(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print("{0} executed in {1}".format(func.__name__, end - start))
        return result
    return wrapper


# JSON TOOL
def json_get_data(json_file):
    """Returns a json data
    """
    with open(json_file) as f:
        json_data = json.load(f)

    return json_data


def json_write_data(json_data, output):
    """Write data into a json file
    """
    with open(output, 'w') as f:
        json.dump(json_data, f, indent=4, encoding='utf-8', sort_keys=True)
        return True
    return False


# XML TOOL
def xml_get_data(xml_file):
    raise NotImplementedError()


def xml_to_string(elt):
    return ctree.tostring(elt)


# CSV TOOL
def csv_get_data(filename, as_dict=False, skip_header=False):
    data = []
    with open(filename, 'rb') as fd:
        read_method = 'DictReader' if as_dict else 'reader'
        rows = vars(csv)[read_method](fd, delimiter=',', quotechar='"')
        if read_method == 'reader' and skip_header:
            rows.next()
        for row in rows:
            data.append(row)

        return data


def csv_get_dict_data(filename, fieldnames=[], delimiter=',', skip_header=False):
    with open(filename, 'rb') as fd:
        reader = csv.DictReader(fd, delimiter=delimiter, quotechar='|', fieldnames=fieldnames)
        if skip_header:
            reader.next()
        return list(reader)
    return False


def csv_write_dict_data(data, filename, fieldnames=[]):
    with open(filename, 'wb') as fd:
        if not fieldnames:
            fieldnames = data[0].keys()
        writer = csv.DictWriter(fd, fieldnames)
        writer.writerows(data)


# JSON/XML prettyfier
def json_pretty(data):
    if isinstance(data, str):
        data = json.loads(data.decode('utf-8'))
    return json.dumps(data, indent=2, sort_keys=True)


def xml_pretty(data):
    parsed_string = minidom.parseString(data.decode('utf-8'))
    return parsed_string.toprettyxml(indent='\t', encoding='utf-8')


# PKG TOOLS
def whereis(pkg):
    return getattr(pkg, '__path__', None)


def show(pkg):
    pass


# UUID
def uuidgen():
    return uuid.uuid4().bytes.encode('base64').rstrip('=\n').replace('/', '_')

# Python-Requests
try:
    import requests

    class LoggedRequest(requests.Session):

        def __init__(self, *args, **kwargs):
            super(LoggedRequest, self).__init__(*args, **kwargs)
            self.logger = logging.getLogger(__name__)

        def request(self, method, url, **kwargs):
            logger.debug('Request\n%s - %s' % (method, url))
            response = super(LoggedRequest, self).request(method, url, **kwargs)
            logger.debug('\n'.join(
                ['%s: %s' % (k, v) for k, v in response.request.headers.items()]
            ))
            logger.debug('Data: %s' % response.request.body)
            logger.debug('\nResponse\n%s' % response.status_code)
            logger.debug('\n'.join(
                ['%s: %s' % (k, v) for k, v in response.headers.items()]
            ))
            logger.debug('Data: %s' % response.content)

            return response

    # Substittude requests
    requests = LoggedRequest()
except (ImportError,) as e:
    pass

# LAODING COMMONS
for common in ('py_common', 'django_common'):
    if os.path.realpath(os.path.join(HOME_SCRIPTS, 'python')) != os.path.realpath('.'):
        try:
            execfile(os.path.join(HOME_SCRIPTS, 'python', common + '.py'))
        except(Exception,) as e:
            logger.error(e.message)
            pdb.set_trace()


# SAVING HISTORY TO FILE
PY_HISTORY_FILE = '.pyhistory'
PY_HISTORY_PATH = os.path.join(HOME_DIR, PY_HISTORY_FILE)
PY_HISTORY_MAX_LENGTH = -1

if not os.path.isfile(PY_HISTORY_PATH):
    with open(PY_HISTORY_PATH, 'w+') as fd:
        pass

readline.set_history_length(PY_HISTORY_MAX_LENGTH)

try:
    readline.read_history_file(PY_HISTORY_PATH)
    logger.info("SHELL HISTORY LOADED")
except (IOError,) as e:
    logger.info("LOADING SHELL HISTORY FAILED")
    logger.error(e.message)
else:
    import atexit
    atexit.register(readline.write_history_file, PY_HISTORY_PATH)
