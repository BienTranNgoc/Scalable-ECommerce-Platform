# Add these imports at the top
import os

from ProjectConfig.settings.base import BASE_DIR

try:
    from botocore.config import Config
except Exception as e:
    pass
else:
    AWS_S3_CLIENT_CONFIG = Config(
        max_pool_connections=int(os.getenv('AWS_S3_MAX_POOL_CONNECTIONS', '20')),
        connect_timeout=int(os.getenv('AWS_S3_CONNECT_TIMEOUT', '10')),   # Connection timeout in seconds
        read_timeout=int(os.getenv('AWS_S3_READ_TIMEOUT', '5')),     # Read timeout in seconds
        retries={
            'max_attempts': 2,  # Retry attempts for failed requests
            'mode': 'standard'  # Retry mode can be 'standard' or 'adaptive'
        }
    )

# Add these settings


AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
# AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME', 'us-east-1')
AWS_S3_ENDPOINT_URL = os.getenv('AWS_S3_ENDPOINT_URL', 'http://127.0.0.1:9000/')

AWS_S3_FILE_OVERWRITE = True
AWS_DEFAULT_ACL = None
AWS_QUERYSTRING_AUTH = True

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
MEDIA_URL = f'{AWS_S3_ENDPOINT_URL}' if bool(int(os.getenv('USE_S3', default='0'))) else '/media/'
DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760

STATIC_MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATIC_MEDIA_URL = '/media/'
STATIC_MEDIA_DIR = 'media'
ADMIN_MEDIA_PREFIX = '/static/admin/'
