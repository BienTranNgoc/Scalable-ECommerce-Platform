import os

CACHES = {
    'default': {
        'BACKEND': os.getenv('CACHE_BACKEND', default='django.core.cache.backends.memcached.PyMemcacheCache'),
        'LOCATION': os.getenv('CACHE_LOCATION')
    },
    'session_cache': {
        'BACKEND': os.getenv('CACHE_BACKEND', default='django.core.cache.backends.memcached.PyMemcacheCache'),
        'LOCATION': os.getenv('CACHE_LOCATION_SESSION', default=os.getenv('CACHE_LOCATION'))
    }
}