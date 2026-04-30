from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed, APIException
from rest_framework import permissions
import requests
import uuid
import json
import jwt
import hashlib
import logging
import datetime

from django.core.cache import cache
from applications.iam_users.models import IAMUser
from applications.iam_users.value_objects import IAMRoleFeature
from core.utils import format_response
from applications.iam_users.exceptions import UnauthorizedException
from applications.iam_users.authentication.secure import encrypt_data, decrypt_data, padding_secret

logger = logging.getLogger(__name__)


class IAMAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # Retrieve the token from the Authorization header
        token = request.headers.get('Authorization')
        if not token:
            # Return None if use multiple authentication methods
            raise AuthenticationFailed('Not found token in request headers')

        # Validate the token and get the user ID
        user_id, username = self.validate_token(token)
        if not user_id:
            raise AuthenticationFailed('Invalid Token or User ID not found')

        user = self.get_user(user_id, username)
        if not user:
            raise AuthenticationFailed('User not found')

        # Return the user and the token to comply with DRF's authentication scheme
        return (user, token)

    def validate_token(self, token):
        import logging
        logger = logging.getLogger('')
        try:
            response = requests.post(
                settings.IAM_TOKEN_VALIDATION_URL,
                headers={'Authorization': token, 'Content-Type': 'application/json', 'GIS': settings.IAM_VALIDATION_GIS}
            )
            logger.info(response.content)
            if response.status_code == 200:
                # TODO: Implement the logic to extract the user ID from the response
                # return '+84366791810', '+84366791810'
                return response.json().get('data').get('user_id'), response.json().get('data').get('username')
            else:
                return None, 'Invalid Token'
        except requests.RequestException as e:
            return None

    def get_user(self, user_id, username):
        return IAMUser(user_id=user_id, username=username)


class IAMLicenseAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # Retrieve the token from the Authorization header
        token = request.headers.get('Authorization')
        if not token:
            # Return None if use multiple authentication methods
            raise AuthenticationFailed('Not found token in request headers')

        license = request.headers.get('License')
        if not token:
            raise AuthenticationFailed('Not found license in request headers')

        # Validate the token and get the user ID
        result = self.validate_token(token, license)
        if not result:
            raise AuthenticationFailed('Invalid Token or User ID not found')
        user_id, username, company_id = result

        user = self.get_user(user_id, username, company_id)
        if not user:
            raise AuthenticationFailed('User not found')

        # Return the user and the token to comply with DRF's authentication scheme
        return (user, token)

    def validate_token(self, token, license):
        try:
            headers = {'Authorization': token, 'License': license, 'Content-Type': 'application/json', 'GIS': settings.IAM_VALIDATION_GIS}
            response = requests.post(
                settings.IAM_TOKEN_VALIDATION_URL,
                headers=headers
            )
            if response.status_code == 200 and response.json().get('data').get('company_id'):
                return response.json().get('data').get('username'), response.json().get('data').get('username'), response.json().get('data').get('company_id')
            else:
                return None
        except requests.RequestException as e:
            return None

    def get_user(self, user_id, username, company_id):
        return IAMUser(user_id=user_id, username=username, company_id=company_id)


class IAMLicenseAuthorization(IAMLicenseAuthentication):
    def authenticate(self, request):
        # Retrieve the token from the Authorization header
        token = request.headers.get('Authorization')
        if not token:
            # Return None if use multiple authentication methods
            raise AuthenticationFailed('Not found token in request headers')

        license = request.headers.get('License')
        if not token:
            raise AuthenticationFailed('Not found license in request headers')

        # Validate the token and get the user ID
        result = self.validate_token(token, license)
        if not result:
            raise AuthenticationFailed('Invalid Token or User ID not found')
        user_id, username, company_id, role_features = result

        user = self.get_user_with_role_features(user_id, username, company_id, role_features)
        if not user:
            raise AuthenticationFailed('User not found')
        # Return the user and the token to comply with DRF's authentication scheme
        return (user, token)

    def validate_token(self, token, license):
        try:
            headers = {'Authorization': token, 'License': license, 'Content-Type': 'application/json', 'GIS': settings.IAM_VALIDATION_GIS}
            response = requests.post(
                settings.IAM_TOKEN_VALIDATION_URL,
                headers=headers
            )
            if response.status_code == 200 and response.json().get('data', {}).get('company_id'):
                data = response.json().get('data')
                role_features = data.get("roles", {}).get("features", [{}])
                role_features = list(map(lambda x: x.get("name", ""), role_features))
                return data.get('username'), data.get('username'), data.get('company_id'), role_features
            else:
                return None
        except requests.RequestException as e:
            return None

    @classmethod
    def get_user_with_role_features(cls, user_id, username, company_id, role_features):
        user = IAMUser(user_id=user_id, username=username, company_id=company_id)
        setattr(user, 'role_features', role_features)
        setattr(user, 'is_authenticated', True)
        return user


class CustomPermissionDenied(APIException):
    status_code = 403  # Replace with your desired status code
    default_detail = 'You do not have permission to perform this action.'
    default_code = 'permission_denied'


class IAMPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_id is not None


class IAMProfileManagementPermission(IAMPermission):
    def has_permission(self, request, view):
        return True
        # permission = super().has_permission(request, view) and IAMRoleFeature.face_profile_management in request.user.role_features
        # if not permission:
        #     raise CustomPermissionDenied('You do not have permission to perform this action.')
        # return permission


class IAMResultStoragePermission(IAMPermission):
    def has_permission(self, request, view):
        permission = super().has_permission(request, view) and IAMRoleFeature.face_result_storage in request.user.role_features
        if not permission:
            raise CustomPermissionDenied('You do not have permission to perform this action.')
        return permission


class IAMServicePermission(IAMPermission):
    def has_permission(self, request, view):
        permission = super().has_permission(request, view) and IAMRoleFeature.face_service in request.user.role_features
        if not permission:
            raise CustomPermissionDenied('You do not have permission to perform this action.')
        return permission


class IAMKeycloakAuthorization(IAMLicenseAuthorization):
    def authenticate(self, request):
        # Retrieve the token from the Authorization header
        token = request.headers.get('Authorization')
        if not (token and token.startswith('Bearer')):
            raise AuthenticationFailed('Not found token in request headers')

        license = request.headers.get('License')
        if not token:
            raise AuthenticationFailed('Not found license in request headers')


        token_parts = token.split(' ')
        if len(token_parts) != 2:
            raise AuthenticationFailed('Access token not valid')

        # Validate token and extract payload
        token_decode = self.decode_access_token(token_parts[1])
        if not token_decode:
            raise AuthenticationFailed('Access token not valid')

        # Validate the token and get the user ID
        result = self.validate_token(token, license)
        if not result:
            raise AuthenticationFailed('Invalid Token or User ID not found')
        user_id, username, company_id, role_features = result

        user = self.get_user_with_role_features(user_id, username, company_id, role_features)
        if not user:
            raise AuthenticationFailed('User not found')
        return (user, token)

    def decode_access_token(self, access_token):
        try:
            public_keys = cache.get('KEYCLOAK_PUBLIC_KEY', [])
            if not public_keys:
                response = requests.get(settings.KEYCLOAK_PUBLIC_KEY_URL)
                public_keys = response.json().get("keys", [])
                cache.set('KEYCLOAK_PUBLIC_KEY', public_keys, settings.PUBLIC_KEY_CACHE_TIME)
            for key in public_keys:
                public_key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(key))
                payload = jwt.decode(access_token, key=public_key,
                                     audience=settings.AUDIENCE_ACCESS_TOKEN, algorithms=["RS256"])
                if payload:
                    return payload
            return None
        except Exception:
            return None


class CustomAuthentication(BaseAuthentication):
    def authenticate(self, request):
        try:
            license_token_auth = IAMLicenseAuthorization().authenticate(request)
            if license_token_auth:
                return license_token_auth
        except AuthenticationFailed:
            pass

        try:
            license_jwt_auth = IAMKeycloakAuthorization().authenticate(request)
            if license_jwt_auth:
                return license_jwt_auth
        except AuthenticationFailed:
            pass

        raise UnauthorizedException('Authentication failed')

class NotFoundKey(Exception):
    def __init__(self, kid, access_token):
        self.kid = kid
        self.access_token = access_token
        # Retry: fetch new keys and try again
        response = requests.get(settings.KEYCLOAK_PUBLIC_KEY_URL)
        public_keys = response.json().get("keys", [])
        cache.set('KEYCLOAK_PUBLIC_KEY', public_keys, settings.PUBLIC_KEY_CACHE_TIME)
        for key in public_keys:
            if key.get('kid') == kid:
                public_key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(key))
                try:
                    payload = jwt.decode(
                        access_token,
                        key=public_key,
                        audience=settings.AUDIENCE_ACCESS_TOKEN,
                        algorithms=[key.get('alg', 'RS256')],
                    )
                    self.payload = payload
                    return
                except Exception as e:
                    logger.error(f"Failed to decode token with refreshed key: {e} with token {access_token}")
        raise Exception(f"Public key with kid {kid} not found after retry with token {access_token}")


class IAMAuthorization(BaseAuthentication):
    def authenticate(self, request):
        # Retrieve the token from the Authorization header
        token = request.headers.get('Authorization')
        license_key = request.headers.get('license')
        if not (token and token.startswith('Bearer')):
            raise UnauthorizedException('Not found token in request headers')

        token_parts = token.split(' ')
        if len(token_parts) != 2:
            raise UnauthorizedException('Access token not valid')

        # Validate token and extract payload
        token_decode = self.decode_access_token(token_parts[1])
        if not token_decode:
            raise UnauthorizedException('Decode token failed')

        username: str = token_decode.get('preferred_username')
        company: dict = token_decode.get('organization', '')
        logger.info(f'Company info from token:{company}')
        if not company:
            token_device_id = token_decode.get('device_id')
            if not (token_device_id and license_key):
                raise UnauthorizedException('Device ID not found in JWT token')
            license_decode = self.decode_license(license_key, token_device_id) or {}
            company_id = license_decode.get('company_id', '')
        else:
            company_id: str = list(company.keys())[0]
        user = self.get_user(username, company_id)
        logger.info(f'User info from authen class:{user}')
        if not user:
            raise UnauthorizedException('User not found')

        return (user, token)

    def get_user(self, username, company_id):
        return IAMUser(username=username, company_id=company_id)

    def decode_access_token(self, access_token):
        try:
            # 1. Decode header to get kid
            unverified_header = jwt.get_unverified_header(access_token)
            kid = unverified_header.get('kid')
            if not kid:
                raise Exception("No 'kid' found in token header.")

            # 2. Get public keys from cache or URL
            public_keys = cache.get('KEYCLOAK_PUBLIC_KEY', [])
            if not public_keys:
                response = requests.get(settings.KEYCLOAK_PUBLIC_KEY_URL)
                public_keys = response.json().get("keys", [])
                cache.set('KEYCLOAK_PUBLIC_KEY', public_keys, settings.PUBLIC_KEY_CACHE_TIME)

            # 2.1 Find key with matching kid
            key = next((k for k in public_keys if k.get('kid') == kid), None)
            if not key:
                # 2.2 Raise custom exception to retry
                raise NotFoundKey(kid, access_token)

            # 3. Decrypt and return result
            public_key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(key))
            payload = jwt.decode(
                access_token,
                key=public_key,
                audience=settings.AUDIENCE_ACCESS_TOKEN,
                algorithms=[unverified_header.get('alg', 'RS256')],
            )
            return payload

        except NotFoundKey as e:
            if hasattr(e, 'payload'):
                return e.payload
            logger.error(f"Key with kid {e.kid} not found for token {access_token}")
            return None
        except Exception as e:
            logger.error(f"Error decoding access token: {e} with token {access_token}")
            return None

    def decode_license(self, license_key, device_id):
        try:
            decrypt_token = LicenseHandler.license_decode(license_key, device_id)
            try:
                payload = jwt.decode(jwt=decrypt_token, key=settings.JWT_SIGN, leeway=datetime.timedelta(days=getattr(settings, "LEEWAY_LICENSE", 365 * 10)), algorithms="HS256")
                return payload
            except jwt.InvalidSignatureError:
                logger.error('Invalid sign key')
        except Exception as e:
            logger.error(f"Failed to decode license: {str(e)}")
        return None


class LicenseHandler:
    @staticmethod
    def license_encode(license_key, key=""):
        key = padding_secret(hashlib.md5(key.encode()).hexdigest())
        license_encrypt = encrypt_data(license_key, key)
        return license_encrypt

    @staticmethod
    def license_decode(license_encrypt, key=""):
        key = padding_secret(hashlib.md5(key.encode()).hexdigest())
        license_key = decrypt_data(str(license_encrypt), key)
        return license_key
