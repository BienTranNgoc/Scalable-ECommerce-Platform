from .base import *  # noqa
import os

SECURE_SSL_REDIRECT = bool(os.getenv("DJANGO_SECURE_SSL_REDIRECT", default=False))
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", default="plh@6i2^gqaee3roufn9w_q_#xcsy-3-zf1ekvbnl+t_+czsy&")
CSRF_TRUSTED_ORIGINS = os.getenv('CSRF_TRUSTED_ORIGINS', default='https://b2b-api-gateway.fcam.vn/*,https://beta-api-gateway.fcam.vn/*').split(',')
# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-secure
SESSION_COOKIE_SECURE = True
# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-secure
CSRF_COOKIE_SECURE = True
# https://docs.djangoproject.com/en/dev/topics/security/#ssl-https
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-seconds
# TODO1: set this to 60 seconds first and then to 518400 once you prove the former works
SECURE_HSTS_SECONDS = 60
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-include-subdomains
# SECURE_HSTS_INCLUDE_SUBDOMAINS = bool(os.getenv("DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS", default=True))
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-preload
# SECURE_HSTS_PRELOAD = bool(os.getenv("DJANGO_SECURE_HSTS_PRELOAD", default=True))
SECURE_HSTS_PRELOAD = False
# https://docs.djangoproject.com/en/dev/ref/middleware/#x-content-type-options-nosniff
SECURE_CONTENT_TYPE_NOSNIFF = bool(os.getenv("DJANGO_SECURE_CONTENT_TYPE_NOSNIFF", default=True))

MIDDLEWARE += ['whitenoise.middleware.WhiteNoiseMiddleware']
STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"
STATIC_URL = '/route-admin/static/'
