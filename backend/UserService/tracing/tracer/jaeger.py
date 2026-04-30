from django.conf import settings

from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, SimpleSpanProcessor

resource = Resource(attributes={
    SERVICE_NAME: settings.SERVICE_NAME
})

jaeger_exporter = JaegerExporter(
    agent_host_name=settings.JAEGER_DOMAIN,
    agent_port=6831
)

provider = TracerProvider(resource=resource)
processor = SimpleSpanProcessor(jaeger_exporter)
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)
