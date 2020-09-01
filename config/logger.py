import os
import time

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGS_DIR = os.path.join(BASE_DIR, 'logs')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'large': {
            'format': '{levelname} {asctime} {pathname} {funcName} {lineno} {message} {filename}',
            'style': '{',
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'small': {
            'format': '{levelname} {asctime} {message} ',
            'style': '{',
            'datefmt': "%d/%b/%Y %H:%M:%S"
        }
    },
    'handlers': {
        'info': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': f"{os.path.join(LOGS_DIR)}/info_{time.strftime('%Y_%m')}.log",
            'formatter': 'large',
        },
        'error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': f"{os.path.join(LOGS_DIR)}/error_{time.strftime('%Y_%m')}.log",
            'formatter': 'large',
        },
        'critical': {
            'level': 'CRITICAL',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': f"{os.path.join(LOGS_DIR)}/error_{time.strftime('%Y_%m')}.log",
            'formatter': 'large',
        },
        'dev_tools_handler': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': f"{os.path.join(LOGS_DIR)}/error_{time.strftime('%Y_%m')}.log",
            'formatter': 'small',
        },
    },
    'loggers': {
        'info_logger': {
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'handlers': ['info'],
            'propagate': True,
        },
        'error_logger': {
            'level': 'ERROR',
            'handlers': ['error'],
            'propagate': True,
        },
        'dev_tools': {
            'level': 'ERROR',
            'handlers': ['dev_tools_handler'],
            'propagate': True,
        },
    },
}
