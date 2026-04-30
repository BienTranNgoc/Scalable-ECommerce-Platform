import requests
import sys
import os
from django.conf import settings
from django.core.cache import cache
from rest_framework.pagination import PageNumberPagination
from rest_framework.utils.urls import replace_query_param, remove_query_param
from django.core.mail import send_mail, get_connection
from django.core.mail import EmailMessage
from django.core.mail.backends.smtp import EmailBackend
from email.mime.application import MIMEApplication

import logging
from tracing.decorators import span_decorator
from opentelemetry import trace
tracer = trace.get_tracer(__name__)
logger = logging.getLogger(__name__)


@span_decorator(tracer=tracer)
def get_config(config_name):
    url = '{}://{}/api/configuration/get-data/'.format(settings.FSS_MANAGEMENT_PROTOCOL, settings.FSS_MANAGEMENT_HOST)
    data = {
        "name": config_name
    }
    headers = {
        "gis": settings.FSS_MANAGEMENT_GIS
    }
    try:
        # cert = getattr(settings, 'CERTIFICATE_FILE_PATH', True)
        response = requests.post(url=url, data=data, headers=headers, verify=False)
        response = response.json()
        if response['result']:
            return response
        else:
            message = response
    except Exception as e:
        logger.error('Error: {}'.format(e))
        message = e
    return {'result': False, 'data': {}, 'message': message}


# def send_email(title, content, _to=None, from_user='', from_pwd='', span=None, allow_send_email=getattr(settings, "IS_SEND_EMAIL", True)):
#     email_config = cache.get("email_info_data", {})
#     if not email_config:
#         email_config_data = get_config("email_info")
#         email_config = email_config_data.get("data", {})
#         if email_config_data.get("result", False):
#             cache.set("email_info_data", email_config, 60 * 60)
#     email_host_user = email_config.get("attribute", {}).get("username", "")
#     email_password = email_config.get("attribute", {}).get("password", "")
#     default_email_to = email_config.get("attribute", {}).get("receiver", settings.EMAIL_RECEIVE_LIST)
#     email_to = default_email_to if _to is None else _to
#     try:
#         if allow_send_email:
#             send_mail(
#                 title, content, email_host_user, email_to,
#                 auth_user=email_host_user, auth_password=email_password, fail_silently=False
#             )
#             return 'Success'
#         else:
#             return 'IS_SEND_EMAIL is False'
#     except Exception as e:
#         return 'Error: {}'.format(e)


def send_email(title, content, _to='receiver_frt_playback', from_user='', from_pwd='', span=None, allow_send_email=getattr(settings, "IS_SEND_EMAIL", True), attachment_path=None):
    email_config = cache.get("email_info_data", {})
    if not email_config:
        email_config_data = get_config("email_info")
        email_config = email_config_data.get("data", {})
        if email_config_data.get("result", False):
            cache.set("email_info_data", email_config, 60 * 60)
    email_host_user = email_config.get("attribute", {}).get("username", "")
    email_password = email_config.get("attribute", {}).get("password", "")
    email_host = email_config.get("attribute", {}).get("host", "")
    email_port = email_config.get("attribute", {}).get("port", "")
    email_host_user = email_config.get("attribute", {}).get("username", "")
    email_password = email_config.get("attribute", {}).get("password", "")
    # Configure email connection once
    email_connection = get_connection(
        host=email_host or settings.EMAIL_HOST_FSOFT,
        port=email_port or settings.EMAIL_PORT_FSOFT,
        username=email_host_user or settings.EMAIL_HOST_USER_FSOFT,
        password=email_password or settings.EMAIL_HOST_PASSWORD_FSOFT,
        use_tls=True
    )
    try:
        with email_connection:
            send_mail(
                subject=title,
                message=content,
                from_email=email_host_user,
                recipient_list=email_config.get("attribute", {}).get(_to, settings.EMAIL_RECEIVE_LIST),
                fail_silently=False,  # Changed to False for better error handling
                auth_user=email_host_user,
                auth_password=email_password,
                connection=email_connection
            )
        return 'Success'
    except Exception as e:
        return 'Error: {} - on line {}'.format(e, sys.exc_info()[-1].tb_lineno)


def format_response(**kwargs):
    code_status = kwargs.get("code_status", 1200)
    result = kwargs.get("result", True) if code_status == 1200 else kwargs.get("result", False)
    message = kwargs.get("message", "Success") if code_status == 1200 else kwargs.get("message", "Failed")
    data = kwargs.get("data", {})
    errors = kwargs.get("errors", [])
    title = kwargs.get("title", "")

    return {
        "code_status": code_status,
        "message": message,
        "result": result,
        "errors": errors,
        "data": data,
        "title": title,
    }


class CustomPagination(PageNumberPagination):
    page_size = 10  # Set the number of items per page
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return {
            'count': self.page.paginator.count,
            'total_page': self.page.paginator.num_pages,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
        }

    def get_next_link(self):
        if not self.page.has_next():
            return None
        url = settings.SERVICE_BASE_URL + self.request.get_full_path()
        page_number = self.page.next_page_number()
        return replace_query_param(url, self.page_query_param, page_number)

    def get_previous_link(self):
        if not self.page.has_previous():
            return None
        url = settings.SERVICE_BASE_URL + self.request.get_full_path()
        page_number = self.page.previous_page_number()
        if page_number == 1:
            return remove_query_param(url, self.page_query_param)
        return replace_query_param(url, self.page_query_param, page_number)
