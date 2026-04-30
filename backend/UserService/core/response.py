from rest_framework import serializers, response


class ResponseFormat:
    def __init__(self, result=True, errors=None, code_status=1200, message="Success", data=None):
        self.result = result
        self.errors = errors if errors else []
        self.code_status = code_status
        self.message = message
        self.data = data if data else {}


class ResponseFormatSerializer(serializers.Serializer):
    result = serializers.BooleanField(default=True)
    errors = serializers.ListField(default=[])
    code_status = serializers.IntegerField(default=1200)
    message = serializers.CharField(default="Success")
    data = serializers.SerializerMethodField(method_name="get_custom_data")

    @classmethod
    def get_custom_data(cls, value=None):
        data = value.data
        if data is None:
            return {}
        if isinstance(data, dict) or isinstance(data, list):
            return data
        raise ValueError("data must be dict or list")


class FormatResponse(response.Response):
    base_format = ResponseFormat
    base_serializer_format = ResponseFormatSerializer

    def __init__(self, data=None, status=None,
                 template_name=None, headers=None,
                 exception=False, content_type=None, **kwargs):
        """
        Alters the init arguments slightly.
        For example, drop 'template_name', and instead use 'data'.

        Setting 'renderer' and 'media_type' will typically be deferred,
        For example being set automatically by the `APIView`.
        """
        format_response = self.base_format(data=data, **kwargs)
        format_response_ser = self.base_serializer_format(format_response)
        super().__init__(None, status=status)

        if isinstance(data, serializers.Serializer):
            msg = (
                'You passed a Serializer instance as data, but '
                'probably meant to pass serialized `.data` or '
                '`.error`. representation.'
            )
            raise AssertionError(msg)

        self.data = format_response_ser.data
        self.template_name = template_name
        self.exception = exception
        self.content_type = content_type

        if headers:
            for name, value in headers.items():
                self[name] = value
