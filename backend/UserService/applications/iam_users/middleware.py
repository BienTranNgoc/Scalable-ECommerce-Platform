import requests
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse


class IAMMiddleware(MiddlewareMixin):
    def process_request(self, request):
        token = request.headers.get('Authorization')
        if token:
            user_id = self.validate_token(token)
            if user_id:
                request.user_id = user_id
            else:
                return JsonResponse({'error': 'Invalid Token'}, status=401)
        else:
            return JsonResponse({'error': 'Authorization header missing'}, status=401)

    def validate_token(self, token):
        try:
            response = requests.get(
                settings.IAM_TOKEN_VALIDATION_URL,
                headers={'Authorization': token, 'Content-Type': 'application/json', 'GIS': settings.IAM_VALIDATION_GIS}
            )
            if response.status_code == 200:
                return response.json().get('user_id')
            else:
                return None
        except requests.RequestException:
            return None
