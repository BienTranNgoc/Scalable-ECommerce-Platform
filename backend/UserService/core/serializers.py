from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers


class ResponseSerializer(serializers.Serializer):
    code_status = serializers.IntegerField(default=1200, help_text="Code status of response, default is 1200 ~ success")
    title = serializers.CharField(default="")
    message = serializers.CharField(default="Success")
    data = serializers.DictField()
    errors = serializers.ListField()
    result = serializers.BooleanField(default=True)

    def to_representation(self, instance):
        self.fields['data'] = instance['data']
        return super(ResponseSerializer, self).to_representation(instance)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


def auto_schema(method='post', request_body_serializer=None, response_serializer=ResponseSerializer, **kwargs):
    return swagger_auto_schema(
        method=method,
        request_body=request_body_serializer,
        responses={200: openapi.Response(description='Response of api', schema=response_serializer)},
        **kwargs
    )