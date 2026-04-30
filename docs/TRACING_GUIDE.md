# Distributed Tracing — Developer Integration Guide

## Tổng quan kiến trúc

```
 ┌─────────────────────────────────────────────────────────────────┐
 │                      REQUEST FLOW                                │
 │                                                                  │
 │  Client ──→ Kong ──→ user-service ──→ order-service             │
 │                           │                  │                   │
 │                      Kafka publish       DB query               │
 │                           │                  │                   │
 │                    notification-svc      payment-svc            │
 │                                                                  │
 │  ← ← ← ← ← ← Tất cả đều có Trace ID chung ← ← ← ← ← ← ← ←  │
 └─────────────────────────────────────────────────────────────────┘

 ┌─────────────────────────────────────────────────────────────────┐
 │                   OBSERVABILITY STACK                            │
 │                                                                  │
 │  App Services ──OTLP gRPC──→ OTel Collector                     │
 │                                    │                            │
 │                          ┌─────────┼─────────┐                 │
 │                          ▼         ▼         ▼                  │
 │                        Jaeger  Prometheus  OpenSearch            │
 │                          │         │         │                   │
 │                          └─────────┼─────────┘                 │
 │                                    ▼                            │
 │                                 Grafana                         │
 │                         (unified observability)                 │
 └─────────────────────────────────────────────────────────────────┘
```

---

## Cách tích hợp vào từng service

### Django Services (Python)

```bash
pip install opentelemetry-sdk \
            opentelemetry-exporter-otlp-proto-grpc \
            opentelemetry-instrumentation-django \
            opentelemetry-instrumentation-psycopg2 \
            opentelemetry-instrumentation-redis \
            opentelemetry-instrumentation-requests
```

```python
# config/tracing.py
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource, SERVICE_NAME, SERVICE_VERSION
from opentelemetry.instrumentation.django import DjangoInstrumentor
from opentelemetry.instrumentation.psycopg2 import Psycopg2Instrumentor
from opentelemetry.instrumentation.redis import RedisInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
import os

def setup_tracing(service_name: str):
    """
    Gọi hàm này 1 lần duy nhất khi app khởi động (trong AppConfig.ready())
    """
    resource = Resource.create({
        SERVICE_NAME: service_name,
        SERVICE_VERSION: os.getenv("OTEL_SERVICE_VERSION", "0.1.0"),
        "deployment.environment": os.getenv("ENVIRONMENT", "local"),
    })

    # OTLPSpanExporter: gửi traces đến OTel Collector qua gRPC
    # Collector sau đó route đến Jaeger (và các backends khác)
    otlp_exporter = OTLPSpanExporter(
        endpoint=os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://otel-collector:4317"),
        insecure=True,  # local dev: không cần TLS
    )

    provider = TracerProvider(resource=resource)
    # BatchSpanProcessor: gom spans lại gửi batch → hiệu năng tốt hơn SimpleSpanProcessor
    provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
    trace.set_tracer_provider(provider)

    # Auto-instrumentation: tự động tạo spans cho Django views, DB queries, HTTP calls
    DjangoInstrumentor().instrument()
    Psycopg2Instrumentor().instrument()   # PostgreSQL queries
    RedisInstrumentor().instrument()       # Redis operations
    RequestsInstrumentor().instrument()    # Outgoing HTTP requests

    return trace.get_tracer(service_name)
```

```python
# apps.py (ví dụ User Service)
from django.apps import AppConfig

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        from config.tracing import setup_tracing
        setup_tracing(service_name="user-service")
```

```python
# Tạo custom spans thủ công khi cần chi tiết hơn
from opentelemetry import trace

tracer = trace.get_tracer(__name__)

def process_payment(order_id: str, amount: float):
    # Span tự động được link vào parent span (từ HTTP request)
    with tracer.start_as_current_span("payment.process") as span:
        # Thêm attributes để filter trong Jaeger UI
        span.set_attribute("order.id", order_id)
        span.set_attribute("payment.amount", amount)
        span.set_attribute("payment.currency", "USD")

        try:
            result = stripe.charge(amount)
            span.set_attribute("payment.status", "success")
            span.set_attribute("payment.transaction_id", result.id)
            return result
        except stripe.CardError as e:
            # Đánh dấu span là lỗi → Jaeger hiển thị màu đỏ
            span.set_status(trace.StatusCode.ERROR, str(e))
            span.record_exception(e)
            raise
```

---

### Go Service (Notification Service)

```go
// tracing/tracing.go
package tracing

import (
    "context"
    "os"

    "go.opentelemetry.io/otel"
    "go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracegrpc"
    "go.opentelemetry.io/otel/sdk/resource"
    sdktrace "go.opentelemetry.io/otel/sdk/trace"
    semconv "go.opentelemetry.io/otel/semconv/v1.21.0"
    "google.golang.org/grpc"
)

func InitTracer(serviceName string) (*sdktrace.TracerProvider, error) {
    ctx := context.Background()

    endpoint := os.Getenv("OTEL_EXPORTER_OTLP_ENDPOINT")
    if endpoint == "" {
        endpoint = "otel-collector:4317"
    }

    exporter, err := otlptracegrpc.New(ctx,
        otlptracegrpc.WithEndpoint(endpoint),
        otlptracegrpc.WithInsecure(),
        otlptracegrpc.WithDialOption(grpc.WithBlock()),
    )
    if err != nil {
        return nil, err
    }

    res := resource.NewWithAttributes(
        semconv.SchemaURL,
        semconv.ServiceName(serviceName),
        semconv.ServiceVersion(os.Getenv("OTEL_SERVICE_VERSION")),
    )

    tp := sdktrace.NewTracerProvider(
        sdktrace.WithBatcher(exporter),
        sdktrace.WithResource(res),
        // Sampler: AlwaysSample cho local, ParentBased cho production
        sdktrace.WithSampler(sdktrace.AlwaysSample()),
    )

    otel.SetTracerProvider(tp)
    return tp, nil
}
```

---

## Kafka Trace Propagation

Khi publish message vào Kafka, bạn cần **inject trace context vào message headers**,
để consumer (Notification Service) có thể **extract context** và tạo spans con đúng chuỗi.

```python
# Producer: inject trace context vào Kafka headers
from opentelemetry import trace, propagate
from opentelemetry.propagators.textmap import DefaultGetter, DefaultSetter

class KafkaHeadersSetter(DefaultSetter):
    def set(self, carrier, key, value):
        carrier[key] = value.encode('utf-8') if isinstance(value, str) else value

def publish_event(topic: str, payload: dict):
    headers = {}
    # Inject current span context vào headers
    propagate.inject(headers, setter=KafkaHeadersSetter())

    producer.produce(
        topic=topic,
        value=json.dumps(payload).encode(),
        headers=list(headers.items()),  # [(key, bytes), ...]
    )
```

```python
# Consumer: extract trace context từ Kafka headers
from opentelemetry.propagators.textmap import DefaultGetter

class KafkaHeadersGetter(DefaultGetter):
    def get(self, carrier, key):
        val = carrier.get(key)
        if val is None:
            return []
        return [val.decode('utf-8') if isinstance(val, bytes) else val]

    def keys(self, carrier):
        return list(carrier.keys())

def consume_event(message):
    headers_dict = dict(message.headers() or [])
    # Extract context → span mới là CON của span producer
    ctx = propagate.extract(headers_dict, getter=KafkaHeadersGetter())

    with tracer.start_as_current_span(
        "notification.process",
        context=ctx,           # ← kết nối span này vào trace gốc!
        kind=trace.SpanKind.CONSUMER
    ) as span:
        span.set_attribute("messaging.system", "kafka")
        span.set_attribute("messaging.destination", message.topic())
        # ... xử lý notification
```

---

## Jaeger UI — Cách đọc Waterfall View

```
Trace: checkout-flow [817ms total]  TraceID: 4bf92f3577b34da6a
│
├─ kong: proxy [2ms]
│
├─ user-service: POST /verify-token [5ms]
│   └─ redis: GET session:abc123 [1ms]
│
├─ order-service: POST /orders [800ms]  ← ĐỎ: bottleneck!
│   ├─ postgres: SELECT * FROM inventory [795ms] ← missing index!
│   └─ kafka: PUBLISH order.created [2ms]
│
└─ payment-service: POST /charge [10ms]
    └─ stripe: API call [8ms]
```

Nhìn vào Waterfall → **ngay lập tức thấy** `postgres SELECT` mất 795ms → missing index.
Không cần đọc log từng service, không cần mò đoán.

---

## Environment Variables cần thêm vào mỗi service

```env
# Trong .env của từng service
OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4317
OTEL_SERVICE_VERSION=0.1.0
ENVIRONMENT=local

# OTel SDK tự đọc biến này để set service name
OTEL_SERVICE_NAME=user-service   # thay đổi theo từng service
```
