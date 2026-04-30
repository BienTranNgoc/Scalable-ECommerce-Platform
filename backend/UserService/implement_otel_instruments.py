# -*- coding: utf-8 -*-
import logging

from opentelemetry.instrumentation.django import DjangoInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor

from tracing.hooks import log_hook, open_telemetry_request_hook, open_telemetry_response_hook, request_lib_response_hook
from tracing.tracers.jaeger import provider


def implement():
    DjangoInstrumentor().instrument(
        tracer_provider=provider,
        request_hook=open_telemetry_request_hook,
        response_hook=open_telemetry_response_hook,
    )
    RequestsInstrumentor().instrument(
        tracer_provider=provider,
        request_hook=open_telemetry_request_hook,
        response_hook=request_lib_response_hook,
    )
    LoggingInstrumentor().instrument(
        tracer_provider=provider,
        set_logging_format=True,
        log_level=logging.INFO,
        log_hook=log_hook,
    )
