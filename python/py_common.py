# module loading py_common.py if found in current dir
import os
import imp
import logging


# when lunching shell
py_common = os.path.join(
    os.path.realpath('.'), 'py_common.py'
)

if os.path.exists(py_common):
    logger.info("LOADING PY_COMMON FILE")
    execfile(py_common)
