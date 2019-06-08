import os
import sys
import pdb
import logging

logger = logging.getLogger('default_logger')

HOME_SCRIPTS_PYTHON = os.path.join(os.environ.get('HOME_SCRIPTS'), 'python')


if sys.version_info.major == 3:
    def execfile(filename):
        code = compile(open(filename, 'rb').read(), filename, 'exec')
        exec(code, globals(), locals())

# LAODING COMMONS
for common in ('py_common', 'django_common'):
    if os.path.realpath(HOME_SCRIPTS_PYTHON) != os.path.realpath('.'):
        try:
            execfile(os.path.join(HOME_SCRIPTS_PYTHON, common + '.py'))
        except(Exception,) as exc:
            logger.exception('ERROR OCCURED')
            pdb.set_trace()

# LOADING IMPORTS
logger.info("COMMON IMPORTS LOADED")
execfile(os.path.join(HOME_SCRIPTS_PYTHON, 'imports.py'))
