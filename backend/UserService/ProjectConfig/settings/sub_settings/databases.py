import os

DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': os.getenv('DB_DEFAULT_NAME'),
        'USER': os.getenv('DB_DEFAULT_USER', ''),
        'PASSWORD': os.getenv('DB_DEFAULT_PASSWORD', ''),
        'HOST': os.getenv('DB_DEFAULT_HOST', ''),
        'PORT': os.getenv('DB_DEFAULT_PORT', ''),
        'CONN_MAX_AGE': int(os.getenv("DB_DEFAULT_CONN_MAX_AGE", 60)),
        'OPTIONS': {
            "connect_timeout": 30
        },
        'TEST': {
            'CHARSET': 'utf8mb4',
            'COLLATION': 'utf8mb4',
        },
    }
}