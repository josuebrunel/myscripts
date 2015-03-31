##################################################
#
#   Author          : yosuke
#   Filename        : __init__.py
#   Description     : 
#   Creation Date   : 09-03-2015
#   Last Modified   : Tue Mar 31 18:20:54 2015
#
##################################################

import os
import imp
import pdb
import time, datetime
from functools import wraps

##AUTO COMPLETION
import readline, rlcompleter
if 'libedit' in readline.__doc__:
    readline.parse_and_bind("bind ^I rl_complete")
else:
    readline.parse_and_bind("tab: complete")


def _myimport_(name, path=None):
    """Handles module import according to a given path
    """
    if not path:
        home_scripts_python = os.path.join(os.environ['HOME_SCRIPTS'],'python')
        path = os.path.join(home_scripts_python,name+'.py')

    if not os.path.isfile(path):
        raise ImportError("No such file : {0}".format(path))

    return imp.load_source(name,path)

db = _myimport_('db')

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

