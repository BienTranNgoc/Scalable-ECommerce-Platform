import sys
import traceback
import logging

from django.conf import settings
from opentelemetry import trace
from rest_framework.exceptions import ValidationError
from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.response import Response
from rest_framework import status, exceptions
from django.utils.translation import gettext_lazy as _


from tracing.decorators import span_decorator

logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)


def custom_exception_handler(exc, context, **kwargs):
    # trace_id = kwargs.get('trace_id', 'Unknown')
    # Call DRF's default exception handler first
    response = drf_exception_handler(exc, context)
    if isinstance(exc, exceptions.APIException):
        response.data = exc.get_full_details()
    if response is not None:
        if response.status_code == status.HTTP_400_BAD_REQUEST:
            response.data = {
                'error': 'Bad request',
                'details': response.data,
            }
        elif response.status_code == status.HTTP_404_NOT_FOUND:
            response.data = {
                'error': 'Not found',
                'details': response.data,
            }
        elif response.status_code == status.HTTP_501_NOT_IMPLEMENTED:
            response.data = {
                'error': 'An unexpected error occurred',
                'details': response.data,
            }
    else:
        tb = traceback.extract_tb(sys.exc_info()[2])
        if tb:
            last_trace = tb[-1]
            line_number = last_trace.lineno
            file_name = last_trace.filename
            function_name = last_trace.name
        else:
            line_number = 'Unknown'
            file_name = 'Unknown'
            function_name = 'Unknown'

        error_details = {
            'type': type(exc).__name__,
            'args': exc.args,
            'message': str(exc),
            'line': line_number,
            'file': file_name,
            'function': function_name
        }
        logger.error('An unexpected error occurred: {}'.format(error_details), exc_info=True)
        response = Response({
            'error': 'An unexpected error occurred',
            'details': error_details if settings.DEBUG else line_number
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return response


class BaseErrorCode:
    @classmethod
    def raise_error(cls, code, *args):
        if not hasattr(cls, 'DESCRIPTION'):
            raise AttributeError(f"{cls.__name__} must define DESCRIPTION dict.")

        template = cls.DESCRIPTION.get(code)

        # Không có template => lỗi nội bộ, không phải lỗi user
        if not template:
            raise ValueError(f"Unknown error code '{code}' in {cls.__name__}")

        try:
            message = template.format(*args)
        except KeyError as e:
            raise ValueError(
                f"Missing parameter '{e.args[0]}' for error message of code '{code}'"
            ) from e

        # Chỉ lỗi hợp lệ mới trả ra cho user
        raise ValidationError(detail=message, code=code)
