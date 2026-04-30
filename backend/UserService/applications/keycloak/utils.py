
import requests
import logging
from apps.keycloak.models import KeycloaKResetPassword, DirectAccessGrant
from django.conf import settings

logger = logging.getLogger(__name__)

class KeycloakAPI:
    url = settings.BASE_KEYCLOAK_URL
    admin_url = settings.KEYCLOAK_ADMIN_URL

    @staticmethod
    def call_api_authenticate(username, password, device_id, otp=None):
        url = f"{KeycloakAPI.url}/token"
        data = DirectAccessGrant(
            username=username,
            password=password,
            client_id=settings.KEYCLOAK_DEV_CLIENT_ID,
            audience=settings.KEYCLOAK_DEV_AUDIENCE,
            device_id=device_id,
            client_secret=settings.KEYCLOAK_SECRET
        )
        request_data = data.__dict__
        response = requests.post(url, data=request_data)
        if response.status_code == 200:
            return response.json()
        else:
            return False

    @staticmethod
    def call_api_reset_password(user_id: str, password: str, access_token: str, temporary: bool = False, headers: dict = {}):
        url = f"{settings.KEYCLOAK_ADMIN_URL}/users/{user_id}/reset-password"
        data = KeycloaKResetPassword(
            temporary=temporary,
            type="password",
            value=password,
        )
        headers.update({
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        })
        import json
        response = requests.put(url, data=json.dumps(
            data.__dict__), headers=headers)
        logger.info(f'Response when update user password: {response.status_code} - {response.text}')
        if response.status_code == 204:
            return True
        else:
            return False

    @staticmethod
    def call_api_logout(id_token: str, headers: dict={}):
        url = f"{KeycloakAPI.url}/logout?id_token_hint={id_token}"
        headers.update({
            'Content-Type': 'application/json',
        })
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return True
        else:
            return False

    @staticmethod
    def call_api_logout_all_session(access_token: str, user_id: str, headers: dict={}):
        url = f"{KeycloakAPI.admin_url}/users/{user_id}/logout"
        headers.update({
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        })
        response = requests.post(url, headers=headers)
        if response.status_code == 204:
            return True
        else:
            return False

    @staticmethod
    def call_api_register_token(username, otp, headers: dict={}):
        url = f"{KeycloakAPI.url}/external-otp/register"
        headers.update({
            'Content-Type': 'application/json',
        })
        data = {
            "username": username,
            "code": otp
        }
        import json
        response = requests.post(url, data=json.dumps(data), headers=headers)
        if response.status_code == 200:
            return True
        else:
            return False
