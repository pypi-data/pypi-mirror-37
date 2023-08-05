"""
Logging configuration module
"""
import logging
from logging.config import dictConfig

FORMATTERS = {
    'verbose': {
        'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    },

    'simple': {
        'format': '%(levelname)s %(message)s'
    },
    'colored_console': {
        '()': 'coloredlogs.ColoredFormatter',
        'format': "%(asctime)s - %(name)s - %(levelname)s - %(message)s", 'datefmt': '%H:%M:%S'
    },
}

HANDLERS = {
    'console': {
        'level': 'DEBUG',
        'class': 'logging.StreamHandler',
        'formatter': 'colored_console'
    },
}

LOGGERS = {
    'ktdk': {'handlers': ['console'], 'level': 'TRACE', 'propagate': True},
    'tests': {'handlers': ['console'], 'level': 'DEBUG', 'propagate': True},
}

LOGGING_CONF = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': FORMATTERS,
    'handlers': HANDLERS,
    'loggers': LOGGERS,
}

TRACE_LOG_LVL = 9


def _trace(self, message, *args, **kws):
    if self.isEnabledFor(TRACE_LOG_LVL):
        # Yes, logger takes its '*args' as 'args'.
        self._log(TRACE_LOG_LVL, message, args, **kws)


def add_custom_log_level():
    logging.addLevelName(TRACE_LOG_LVL, 'TRACE')
    logging.Logger.trace = _trace


def load_config():
    """Loads config based on the config type
    """
    add_custom_log_level()
    dictConfig(LOGGING_CONF)
