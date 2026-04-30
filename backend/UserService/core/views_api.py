from rest_framework import viewsets
from rest_framework.response import Response

from core.serializers import ResponseSerializer


class BaseViewSet(viewsets.ViewSet):
    def response(self, data, status=None):
        serializer = ResponseSerializer(data=data)
        serializer.is_valid()
        return Response(serializer.data, status=status)
