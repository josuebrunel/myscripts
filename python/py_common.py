# module loading py_common.py if found in current dir
import os
import imp
import logging

def load_common(common):
    """loads dj_common.py
    """
    try:
        module = imp.load_source('common', common)
        return module
    except (ImportError,) as e:
        logging.error(e)
        return None

# when lunching shell
py_common = os.path.join(
    os.path.realpath('.'), 'py_common.py'
)

if os.path.exists(py_common):
    common = load_common(py_common)
    if common :
        from common import *

