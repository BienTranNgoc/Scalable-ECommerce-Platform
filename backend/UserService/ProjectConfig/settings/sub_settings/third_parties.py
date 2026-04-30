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

ROGO_PROTOCOL = env.str('ROGO_PROTOCOL', default='https')
ROGO_HOST = env.str('ROGO_HOST', default='api.rogo.io')
ROGO_API_V2_PREFIX = env.str('ROGO_API_V2_PREFIX', default='api/v2')
ROGO_API_KEY = env.str('ROGO_API_KEY', default='')
