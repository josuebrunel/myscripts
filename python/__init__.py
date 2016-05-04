##################################################
#
#   Author          : josuebrunel
#   Filename        : __init__.py
#   Description     :
#   Creation Date   : 09-03-2015
#   Last Modified   : Fri 18 Mar 2016 09:43:45 AM CET
#
##################################################

import os
import sys
import imp
import pdb
import json
import uuid
import time, logging, datetime
from functools import wraps
from xml.dom import minidom
from pprint import pprint as pp

from importlib import import_module

##AUTO COMPLETION
import readline, rlcompleter
if 'libedit' in readline.__doc__:
    readline.parse_and_bind("bind ^I rl_complete")
else:
    readline.parse_and_bind("tab: complete")

HOME_DIR = os.environ.get('HOME')
HOME_SCRIPTS = os.environ['HOME_SCRIPTS']

if sys.version_info < (3.0,):
    execfile(os.path.join(HOME_SCRIPTS, 'python', 'db.py'))


#USEFUL METHOD
def get_real_path(f):
    """Retuns the realpath of a file
    """
    return os.path.realpath(f)

def get_joined_path(a, b):
    """Returns joined path of to file
    """
    return os.path.join(a,b)

def get_file_content(filename):
    """Returns content of a given file
    """
    with open(filename) as f :
        return f.read()

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
        json.dump(json_data, f, indent= 4, encoding= 'utf-8', sort_keys=True)
        return True
    return False

# XML TOOL
def xml_get_data(xml_file):
    pass

# JSON/XML prettyfier
def json_pretty(data):
    if isinstance(data, str):
        data = json.loads(data.decode('utf-8'))
    return json.dumps(data, indent=2, sort_keys=True)

def xml_pretty(data):
    parsed_string = minidom.parseString(data.decode('utf-8'))
    return parsed_string.toprettyxml(indent='\t', encoding='utf-8')

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
            print('Request\n%s - %s' %(method, url))
            response = super(LoggedRequest, self).request(method, url, **kwargs)
            print('\n'.join(
                ['%s: %s' %(k,v) for k,v in response.request.headers.items()]
            ))
            print('Data: %s' %response.request.body)
            print('\nResponse\n%s' %response.status_code)
            print('\n'.join(
                ['%s: %s' %(k,v) for k,v in response.headers.items()]
            ))
            print('Data: %s' %response.content)

            return response

    # Substittude requests
    requests = LoggedRequest()
except (ImportError,) as e:
    pass

# LAODING COMMONS
for common in ('py_common', 'django_common'):
    if os.path.realpath(
        os.path.join( HOME_SCRIPTS, 'python')) != os.path.realpath('.'):
        execfile(os.path.join(HOME_SCRIPTS, 'python', common+'.py'))

## SAVING HISTORY TO FILE
PY_HISTORY_FILE = '.pyhistory'
PY_HISTORY_PATH = os.path.join(HOME_DIR, PY_HISTORY_FILE)

if not os.path.isfile(PY_HISTORY_PATH):
    with open(PY_HISTORY_PATH, 'w+') as fd:
        pass

try:
    logging.info("LOADING PYTHON SHELL HISTORY")
    readline.read_history_file(PY_HISTORY_PATH)
except (IOError,) as e:
    logging.error("LOADING OF PYTHON SHELL HISTORY FAILED")
    logging.error(e)
else:
    import atexit
    atexit.register(readline.write_history_file, PY_HISTORY_PATH)

