##################################################
#
#   Author          : josuebrunel
#   Filename        : __init__.py
#   Description     :
#   Creation Date   : 09-03-2015
#   Last Modified   : Fri 29 Jan 2016 02:20:48 PM CET
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

def load_module(name, path=None):
    """Handles module import according to a given path
    """
    if not path:
        home_scripts_python = os.path.join(os.environ['HOME_SCRIPTS'],'python')
        path = os.path.join(home_scripts_python,name+'.py')

    if not os.path.isfile(path):
        raise ImportError("No such file : {0}".format(path))

    return imp.load_source(name,path)

if sys.version_info < (3.0,):
    db = load_module('db')

# LAODING DJANGO STUFF
try:
    django_utils = load_module('django_utils')
    from django_utils import *
except ImportError:
    logging.info("No Django Config Found")

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
    data = json.loads(data.decode('utf-8'))
    return json.dumps(data, indent=2, sort_keys=True)

def xml_pretty(data):
    parsed_string = minidom.parseString(data.decode('utf-8'))
    return parsed_string.toprettyxml(indent='\t', encoding='utf-8')

# UUID
def uuidgen():
    return uuid.uuid4().bytes.encode('base64').rstrip('=\n').replace('/', '_')


## SAVING HISTORY TO FILE
HOME_DIR = os.environ.get('HOME')
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

