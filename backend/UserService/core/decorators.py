import logging
import time
from functools import wraps

from django.db import OperationalError, connections

logger = logging.getLogger(__name__)


def validate_request(serializer_class):
    def decorator(func):
        @wraps(func)
        def wrapper(self, request, *args, **kwargs):
            instance = None
            if 'pk' in kwargs:  # Là detail view
                instance = self.get_object()

            serializer = serializer_class(
                instance=instance,
                data=request.data,
                context={'request': request}
            )
            serializer.is_valid(raise_exception=True)

            return func(self, request, serializer.validated_data, *args, **kwargs)

        return wrapper
    return decorator


def safe_query(max_retries: int = 3, base_delay: int = 1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            delay = base_delay
            for attempt in range(max_retries):
                try:
                    connections.close_all()
                    return func(*args, **kwargs)
                except OperationalError as e:
                    if attempt < max_retries - 1:
                        logger.warning(
                            f"DB error (attempt {attempt+1}/{max_retries}): {e}"
                        )
                        time.sleep(delay)
                        delay *= 2
                    else:
                        logger.error(
                            f"DB failed after {max_retries} attempts: {e}"
                        )
                        raise
        return wrapper
    return decorator
