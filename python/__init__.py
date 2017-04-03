import os
import sys
import pdb
import logging
import readline
import rlcompleter
from logging.config import dictConfig


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
    execfile(os.path.join(HOME_SCRIPTS_PYTHON, 'db.py'))

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
        except(Exception,) as e:
            logger.error(e.message)
            pdb.set_trace()

# LOADING IMPORTS
logger.info("COMMON IMPORTS LOADED")
execfile(os.path.join(HOME_SCRIPTS_PYTHON, 'imports.py'))

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
