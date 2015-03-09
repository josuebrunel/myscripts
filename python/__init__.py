##################################################
#
#   Author          : yosuke
#   Filename        : __init__.py
#   Description     : 
#   Creation Date   : 09-03-2015
#   Last Modified   : Mon 09 Mar 2015 06:08:57 AM CDT
#
##################################################

import os
import imp

def myimport(name, path):
    """Handles module import according to a given path
    """
    home_scripts_python = os.path.join(os.environ['HOME_SCRIPTS'],'python')
    return imp.load_source(name,os.path.join(home_scripts_python,path))

db = myimport('db','db.py')

##AUTO COMPLETION
import readline, rlcompleter
if 'libedit' in readline.__doc__:
    readline.parse_and_bind("bind ^I rl_complete")
else:
    readline.parse_and_bind("tab: complete")

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

