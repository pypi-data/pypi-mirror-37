import logging
import sys


LOGGING_CONFIG_DEFAULTS = dict(
    version=1,
    disable_existing_loggers=False,

    loggers={
        'pahotoolkit': {
            'level': 'DEBUG',
            'handlers': ['console']
        },
        'pahotoolkit_error': {
            'level': 'INFO',
            'handlers': ['error_console'],
            'propagate': True,
            'qualname': 'error'
        },
    },
    handlers={
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'generic',
            'stream': sys.stdout
        },
        'error_console': {
            'class': 'logging.StreamHandler',
            'formatter': 'generic',
            'stream': sys.stderr
        },
    },
    formatters={
        'generic': {
            'format': '[%(process)d - %(thread)d - %(module)s - %(funcName)s] [%(levelname)s] %(message)s',  # noqa
            'class': 'logging.Formatter'
        },
    }
)

logger = logging.getLogger('pahotoolkit')

error_logger = logging.getLogger('pahotoolkit_error')
