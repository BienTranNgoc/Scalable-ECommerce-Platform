import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent.parent

IS_CONSOLE_LOG = bool(os.getenv('IS_CONSOLE_LOG', True))

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y-%H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
        'verbose2': {
            'format': "[%(asctime)s]___%(levelname)s___[%(name)s:%(lineno)s]___%(message)s",
            'datefmt': "%d/%b/%Y-%H:%M:%S"
        },
        'verbose3': {
            'format': "[%(asctime)s]___%(levelname)s___[%(name)s:%(lineno)s]___%(message)s",
            'datefmt': "%d/%b/%Y-%H:%M:%S"
        },
        "verbose_important": {
            'format': "%(asctime)s___%(levelname)s___%(message)s",
            'datefmt': "%d/%m/%Y-%H:%M:%S"
        }
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'api.log'),
            'formatter': 'verbose'
        },
        'error': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'error.log'),
            'when': 'D',
            'interval': 1,
            'backupCount': 10,
            'formatter': 'verbose',
        },
        'django': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': os.path.join(BASE_DIR, 'logs', 'django.log'),
        },
        "check_log": {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'face', 'check.log'),
            "formatter": "verbose_important"
        },
        "attendance_log": {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'face', 'attendance.log'),
            "formatter": "verbose_important"
        },
        "service_health_log": {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'face', 'check_health.log'),
            "formatter": "verbose_important"
        },
        "export_log": {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'face', 'export.log'),
            "formatter": "verbose_important"
        },
        "console_info": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
            "stream": "ext://sys.stdout",
        },
        "console_error": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
            "stream": "ext://sys.stderr",
        },
        "forward_mqtt_log": {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'face', 'forward.log'),
            "formatter": "verbose_important"
        }
    },
    'loggers': {
        '': {
            'handlers': ['console_info' if IS_CONSOLE_LOG else 'file'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
        'root': {
            'handlers': ['console_info' if IS_CONSOLE_LOG else 'file'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
        'check_face_result': {
            'handlers': ['console_info' if IS_CONSOLE_LOG else 'check_log'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
        'process_attendance': {
            'handlers': ['console_info' if IS_CONSOLE_LOG else 'attendance_log'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
        'check_file_export': {
            'handlers': ['console_info' if IS_CONSOLE_LOG else 'export_log'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
        'forward_mqtt': {
            'handlers': ['console_info' if IS_CONSOLE_LOG else 'forward_mqtt_log'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
        'check_face_service_health': {
            'handlers': ['console_info' if IS_CONSOLE_LOG else 'service_health_log'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
    },
}