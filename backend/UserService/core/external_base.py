import requests
import json
from django.conf import settings

from core.utils import send_email

import logging
from tracing.decorators import span_decorator
from opentelemetry import trace

tracer = trace.get_tracer(__name__)
logger = logging.getLogger("")
global_logger = logging.getLogger("")


class RequestFetch(object):
    POST = "POST"
    GET = "GET"
    PUT = "PUT"
    DELETE = "DELETE"

    service_name = "request_base"
    host_name = "localhost"
    gis = ""
    protocol = "http"

    def __init__(self):
        self.base_url = "{}://{}".format(self.protocol, self.host_name)

    @classmethod
    def check_response(cls, response, func_name, body, logger=None):
        if response.get("http_status", 0) != 200:
            title = '[{}] '.format(getattr(settings, 'SERVICE_NAME', 'prodCustomer')) + 'Alert call api {} failed'.format(func_name)
            send_email(title, "Error get when {} with body {}. Check connection between Customer service and Cloud service".format(func_name, json.dumps(body)))
        elif not response.get("result", False):
            logger.error("Error get when {} with body {}. Check connection between Customer service and Management service".format(func_name, json.dumps(body)))

    def get_header(self, header=None):
        default_header = {}
        if self.gis:
            default_header.update({
                "gis": self.gis
            })
        if header:
            default_header.update(header)
        return default_header

    @span_decorator(tracer=tracer)
    def fetch(self, uri, body, logger=None, header=None, method="post", timeout=10, log_resp=True, req_data=None):
        if not logger:
            logger = global_logger
        full_url = self.base_url + uri
        # full_url = uri
        func_call = getattr(requests, method)
        header = self.get_header(header)
        func_name = "_".join(uri.split("/"))
        logger.info("call {} with url {} body {}".format(func_name, full_url, body))
        data = {
            "result": False
        }
        try:
            if req_data:
                logger.info("call {} with url {} data {}".format(func_name, full_url, req_data))
                response = func_call(full_url, data=req_data, headers=header, verify=False, timeout=timeout)
            else:
                response = func_call(full_url, json=body, headers=header, verify=False, timeout=timeout)
            data.update(http_status=response.status_code)
            if response.status_code != 200:
                title = '[{}] '.format(settings.SERVICE_NAME) + 'Warning fetch api failed'
                send_email(title, "Error fetching {} with body {}. Check connection between Customer service and {} service".format(uri, json.dumps(body), self.service_name))

        except Exception as e:
            logger.error("call {} error with url {}".format(e, full_url))
        else:
            try:
                data.update(response.json())
            except Exception as e:
                logger.warning("parse data error with {}".format(response.content))
            else:
                if log_resp:
                    logger.info('API {} SUCCESS: {}'.format(data, full_url))
        return data

    @span_decorator(tracer=tracer)
    def request(self, uri, body, logger=None, header=None, method='POST', timeout=10, log_resp=True, req_data=None, files={}):
        if not logger:
            logger = global_logger
        full_url = "{}/{}".format(self.base_url, uri)
        header = self.get_header(header)
        func_name = "_".join(uri.split("/"))
        logger.info("call {} with url {} body {}".format(func_name, full_url, body))
        data = {
            "result": False
        }
        try:
            if req_data:
                logger.info("call {} with url {} data {}".format(func_name, full_url, req_data))
                response = requests.request(method, full_url, data=req_data, headers=header, verify=False, timeout=timeout, files=files)
            elif files:
                for key, value in body.items():
                    files[key] = value
                response = requests.request(method, full_url, data=body, headers=header, files=files, timeout=timeout, verify=False)
            else:
                response = requests.request(method, full_url, data=body, headers=header, verify=False, timeout=timeout, files=files)
            data.update(http_status=response.status_code)
            if response.status_code != 200:
                title = '[{}] '.format(settings.SERVICE_NAME) + 'Warning fetch api failed'
                send_email(title, "Error fetching {} with body {}. Check connection between Customer service and {} service".format(uri, json.dumps(body), self.service_name))

        except Exception as e:
            logger.error("call {} error with url {}".format(e, full_url))
        else:
            try:
                data.update({
                    'result': True,
                    'response': response
                })
            except Exception as e:
                logger.warning("parse data error with {}".format(response.content))
            else:
                if log_resp:
                    logger.info('API {} SUCCESS: {}'.format(data, full_url))
        return data


class OpenSearchRequestFetch(object):
    POST = "post"
    GET = "get"
    PUT = "put"
    DELETE = "delete"

    service_name = "request_base"
    host_name = "localhost"
    gis = ""
    protocol = "http"

    def __init__(self):
        self.base_url = "{}://{}".format(self.protocol, self.host_name)

    @classmethod
    def check_response(cls, response, func_name, body, logger=None):
        if response.get("http_status", 0) not in settings.HTTP_STATUS_CODES.get("success", {}).values():
            # title = '[{}] '.format(getattr(settings, 'SERVICE_NAME', 'prodAiFaceReg')) + 'Alert call api {} failed'.format(func_name)
            # send_email(title, "Error get when {} with body {}. Check connection between CADs service and Management service".format(func_name, json.dumps(body)))
            logger.error("Error get when {} with body {}. Check connection between {} service and OpenSearch service".format(func_name, json.dumps(body), getattr(settings, 'SERVICE_NAME', 'prodAiFaceReg')))
        else:
            response.update({"result": True})

    def get_header(self, header=None):
        default_header = {}
        if self.gis:
            default_header.update({
                "gis": self.gis
            })
        if header:
            default_header.update(header)
        return default_header

    @span_decorator(tracer=tracer)
    def fetch(self, uri, body, logger=None, header=None, method="post", timeout=10, log_resp=True, req_data=None):
        if not logger:
            logger = global_logger
        # full_url = "{}/{}".format(self.base_url, uri)
        full_url = uri
        func_call = getattr(requests, method)
        header = self.get_header(header)
        func_name = "_".join(uri.split("/"))
        logger.info("call {} with url {} body {}".format(func_name, full_url, body))
        data = {
            "result": False
        }
        try:
            response = func_call(full_url, json=body, headers=header, verify=False, timeout=timeout, auth=(settings.OPEN_SEARCH_USERNAME, settings.OPEN_SEARCH_PASSWORD))
            data.update(http_status=response.status_code)
            self.check_response(data, func_name, body, logger)
        except Exception as e:
            logger.error("call {} error with url {}".format(e, full_url))
        else:
            try:
                data_read = json.loads(response.content)
                data.update(data_read)
            except Exception as e:
                logger.warning("parse data error with {}".format(response.content))
            else:
                if log_resp:
                    logger.info('API {} SUCCESS: {}'.format(data, full_url))
        return data


class RequestFetchV2(object):
    POST = "post"
    GET = "get"
    PUT = "put"
    DELETE = "delete"

    service_name = "request_base"
    host_name = "localhost"
    gis = ""
    protocol = "http"

    def __init__(self):
        self.base_url = "{}://{}".format(self.protocol, self.host_name)

    @classmethod
    def check_response(cls, response, func_name, body, logger=None):
        if response.get("http_status", 0) not in settings.HTTP_STATUS_CODES.get("success", {}).values():
            # title = '[{}] '.format(getattr(settings, 'SERVICE_NAME', 'prodAiFaceReg')) + 'Alert call api {} failed'.format(func_name)
            # send_email(title, "Error get when {} with body {}. Check connection between CADs service and Management service".format(func_name, json.dumps(body)))
            logger.error("Error get when {} with body {}. Check connection between {} service and OpenSearch service".format(func_name, json.dumps(body), getattr(settings, 'SERVICE_NAME', 'prodAiFaceReg')))
        else:
            response.update({"result": True})

    def get_header(self, header=None):
        default_header = {}
        if self.gis:
            default_header.update({
                "gis": self.gis
            })
        if header:
            default_header.update(header)
        return default_header

    @span_decorator(tracer=tracer)
    def fetch(self, uri, body, logger=None, header=None, method="post", timeout=10, log_resp=True, req_data=None):
        if not logger:
            logger = global_logger
        # full_url = "{}/{}".format(self.base_url, uri)
        full_url = uri
        func_call = getattr(requests, method)
        header = self.get_header(header)
        func_name = "_".join(uri.split("/"))
        logger.info("call {} with url {} body {}".format(func_name, full_url, body))
        data = {
            "result": False
        }
        try:
            response = func_call(full_url, json=body, headers=header, verify=False, timeout=timeout)
            data.update(http_status=response.status_code)
            self.check_response(data, func_name, body, logger)
        except Exception as e:
            logger.error("call {} error with url {}".format(e, full_url))
        else:
            try:
                data_read = json.loads(response.content)
                data.update(data_read)
            except Exception as e:
                logger.warning("parse data error with {}".format(response.content))
            else:
                if log_resp:
                    logger.info('API {} SUCCESS: {}'.format(data, full_url))
        return data
