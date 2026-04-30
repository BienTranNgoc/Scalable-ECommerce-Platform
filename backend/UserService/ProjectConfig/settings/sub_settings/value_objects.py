import environ
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
env = environ.Env()
READ_DOT_ENV_FILE = env.bool("DJANGO_READ_DOT_ENV_FILE", default=True)
if READ_DOT_ENV_FILE:
    # OS environment variables take precedence over variables from .env
    # env.read_env(str(BASE_DIR / ".envs" / f".env.{env.str('ENVIRONMENT_SETTING', 'local')}"))
    env.read_env(os.path.join(BASE_DIR, '.env'))


MAX_PLACES_IN_USER = env.int('MAX_PLACES_IN_USER', default=5)
MAXIMUM_GROUP_LEVEL = env.int('MAXIMUM_GROUP_LEVEL', default=5)
USER_ACCESS_CACHE_KEY = "user_{}_company_{}"
SUBJECT_ACLS_CACHE_PATTERN = "subject_{}_content_type_{}_object_id_{}"
ROLE_FEATURES_CACHE_PATTERN = "role_{}"
UAC_RESOURCES = "uac_{}_resources"
