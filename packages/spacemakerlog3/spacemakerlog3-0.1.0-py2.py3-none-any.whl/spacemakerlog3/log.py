import logging.config
import structlog

logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'json': {
            'format': '%(message)s %(lineno)d %(pathname)s',
            'class': 'pythonjsonlogger.jsonlogger.JsonFormatter'
        }
    },
    'handlers': {
        'json': {
            'class': 'logging.StreamHandler',
            'formatter': 'json'
        }
    },
    'loggers': {
        '': {
            'handlers': ['json'],
            'level': logging.INFO
        }
    }
})


def _dict_to_log(d):
    """
    Recursively create log in key=value pairs (text format)
    output for nested dictionaries.
    """
    arr = []
    for k, v in d.items():
        val = v
        if isinstance(v, dict):
            val = '[{}]'.format(_dict_to_log(v))
        arr.append('{}={}'.format(k, val))
    return ' '.join(arr)


def _add_kwargs(logger, method_name, event_dict):
    """
    Add **kwargs to text format output
    """
    d = dict(event_dict)
    del d['event']
    del d['level']
    del d['timestamp']
    event_dict['event'] = event_dict['event'] + ' ' + _dict_to_log(d)
    return event_dict


def _add_exc_info(logger, method_name, event_dict):
    if 'exception' in event_dict:
        event_dict['exc_info'] = True
    return event_dict


structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_log_level,
        _add_exc_info,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso", utc=True, key="timestamp"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        _add_kwargs,
        structlog.stdlib.render_to_log_kwargs,
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

_log = structlog.getLogger()

_levels = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warn": logging.WARN,
    "error": logging.ERROR,
}


def set_format(fmt):
    """
    Set the log format

    :param string fmt: "json" or "text"
    """
    # NB: Only "json" is supported


def set_level(lvl):
    """
    Set the log level

    :param string lvl: "debug", "info", "warn" or "error"
    """
    _log.setLevel(_levels[lvl])


def set_level_external(lvl):
    """
    Set the log level for "external" loggers

    :params string lvl: "debug", "info", "warn" or "error"
    """
    for logger_name in logging.getLogger().manager.loggerDict.keys():
        logging.getLogger(logger_name).setLevel(_levels[lvl])


def debug(msg, *args, **kwargs):
    """
    Log a message with level 'debug'
    """
    try:
        _log.debug(msg, *args, **kwargs)
    except Exception as e:
        _log.debug(msg, log_error=e)


def info(msg, *args, **kwargs):
    """
    Log a message with level 'info'
    """
    try:
        _log.info(msg, *args, **kwargs)
    except Exception as e:
        _log.info(msg, log_error=e)


def warn(msg, *args, **kwargs):
    """
    Log a message with level 'warn'
    """
    try:
        _log.warn(msg, *args, **kwargs)
    except Exception as e:
        _log.warn(msg, log_error=e)


def error(msg, *args, **kwargs):
    """
    Log a message with level 'error'
    """
    try:
        _log.error(msg, *args, **kwargs)
    except Exception as e:
        _log.error(msg, log_error=e)
