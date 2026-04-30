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

UPLOAD_AVATAR_FOLDER = env.str('UPLOAD_AVATAR_FOLDER', default='avatars')
UPLOAD_SERVICE_BACKGROUND_FOLDER = env.str(
    'UPLOAD_SERVICE_BACKGROUND_FOLDER',
    default='backgrounds')
