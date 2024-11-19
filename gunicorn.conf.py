from resin_shared_library.log import LOG_DATE_FORMAT, LOG_MESSAGE_FORMAT, env_is_dev, log_level

bind = '0.0.0.0:80'
dev_env = env_is_dev()
reload = dev_env
worker_class = 'uvicorn.workers.UvicornWorker'
workers = 1 if dev_env else 4
max_requests = 2048
max_requests_jitter = 256

accesslog = '-' if dev_env else None
level = log_level()

logconfig_dict = {
    'version': 1,
    'formatters': {
        'generic': {
            'format': LOG_MESSAGE_FORMAT,
            'datefmt': LOG_DATE_FORMAT,
            'class': 'logging.Formatter',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'generic',
            'stream': 'ext://sys.stdout',
        },
    },
    'loggers': {
        'root': {
            'level': level,
            'handlers': ['console']
        },
        'gunicorn.error': {
            'level': level,
            'handlers': ['console'],
            'propagate': False,
        },
        'event_bus_sdk': {
            'level': level,
            'handlers': ['console'],
            'propagate': False,
        },
    },
}
