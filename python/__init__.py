import os
import logging
import platform
import readline
import rlcompleter
from logging.config import dictConfig
import sys


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
    },
    'formatters': {
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propragate': True,
        }
    }
}

if platform.system() == 'Linux':
    LOGGING['handlers']['syslog'] = {
        'level': 'DEBUG',
        'address': '/dev/log',
        'class': 'logging.handlers.SysLogHandler',
        'formatter': 'syslog',
    }
    LOGGING['formatters']['syslog'] = {
        'format': '%(levelname)s %(name)s.%(funcName)s: %(message)s',
    }
    LOGGING['loggers']['']['handlers'] += ['syslog']

dictConfig(LOGGING)

logger = logging.getLogger('default_logger')


# AUTO COMPLETION
logger.info("SETTING UP AUTOCOMPLETION")
if 'libedit' in readline.__doc__:
    readline.parse_and_bind("bind ^I rl_complete")
else:
    readline.parse_and_bind("tab: complete")

# LOAD PERSONAL UTILS MODULE
py_common = os.path.join(
    os.path.realpath('.'), 'py_common.py'
)

if os.path.exists(py_common):
    logger.info("LOADING PY_COMMON FILE")
    try:
        if sys.version_info.major == 3:
            exec(open(py_common).read())
        else:
            execfile(py_common)
    except(Exception,) as exc:
        logger.exception('ERROR OCCURED: %s' % (exc))


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
