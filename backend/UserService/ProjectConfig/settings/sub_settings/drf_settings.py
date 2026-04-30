import os
from datetime import timedelta

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'core.authentication_classes.KeycloakJWTAuthentication',
    ),
    'EXCEPTION_HANDLER': 'core.exceptions.custom_exception_handler',
}

# JWKS endpoint of Keycloak
# Format: http://<keycloak-host>:<port>/realms/<realm-name>/protocol/openid-connect/certs
KEYCLOAK_JWKS_URL = os.environ.get('KEYCLOAK_JWKS_URL', 'http://localhost:8080/realms/master/protocol/openid-connect/certs')

SIMPLE_JWT = {
    'ALGORITHM': 'RS256',
    'JWK_URL': KEYCLOAK_JWKS_URL,
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'sub',
}
