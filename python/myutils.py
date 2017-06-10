import os
import sys
import pdb
import logging

logger = logging.getLogger('default_logger')

HOME_SCRIPTS_PYTHON = os.path.join(os.environ.get('HOME_SCRIPTS'), 'python')


py_version = sys.version_info[0]

if py_version > 2:
    def execfile(filename):
        with open(filename) as fd:
            code = compile(fd.read(), filename, 'exec')
            exec(code, globals(), locals())

# LOADING LiteORM
execfile(os.path.join(HOME_SCRIPTS_PYTHON, 'orm.py'))

# LOADING FUNCTIONS
logger.info("COMMON FUNCTIONS LOADED")
execfile(os.path.join(HOME_SCRIPTS_PYTHON, 'functions.py'))

# LOADING CLASSES
logger.info("COMMON CLASSES LOADED")
execfile(os.path.join(HOME_SCRIPTS_PYTHON, 'classes.py'))

# LAODING COMMONS
for common in ('py_common', 'django_common'):
    if os.path.realpath(HOME_SCRIPTS_PYTHON) != os.path.realpath('.'):
        try:
            execfile(os.path.join(HOME_SCRIPTS_PYTHON, common + '.py'))
        except(Exception,) as exc:
            logger.error(exc)
            print(exc)
            pdb.set_trace()

# LOADING IMPORTS
logger.info("COMMON IMPORTS LOADED")
execfile(os.path.join(HOME_SCRIPTS_PYTHON, 'imports.py'))
