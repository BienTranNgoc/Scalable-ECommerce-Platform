def span_decorator(tracer):
    def decorator(func):
        def inner(*args, **kwargs):
            with tracer.start_as_current_span(func.__name__) as span:
                return func(*args, **kwargs)
        return inner
    return decorator
