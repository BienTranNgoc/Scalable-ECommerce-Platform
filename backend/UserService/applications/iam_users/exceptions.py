from rest_framework.exceptions import APIException
from rest_framework import status

class UnauthorizedException(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = 'Authentication failed'
    default_code = 'unauthorized'
