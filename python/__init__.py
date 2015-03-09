##################################################
#
#   Author          : yosuke
#   Filename        : __init__.py
#   Description     : 
#   Creation Date   : 09-03-2015
#   Last Modified   : Mon 09 Mar 2015 06:02:14 AM CDT
#
##################################################

import os
import imp

def myimport(name, path):
    """
    """
    home_scripts_python = os.path.join(os.environ['HOME_SCRIPTS'],'python')
    return imp.load_source(name,os.path.join(home_scripts_python,path))

#pythonenv = myimport('pythonenv','pythonenv.py')
db = myimport('db','db.py')

#from pythonenv import *
from db import *
