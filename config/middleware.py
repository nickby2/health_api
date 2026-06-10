import logging
import time


logger = logging.getLogger("api.requests")


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        started_at = time.monotonic()
        response = self.get_response(request)
        elapsed_ms = round((time.monotonic() - started_at) * 1000, 2)
        logger.info(
            "%s %s %s %sms",
            request.method,
            request.path,
            response.status_code,
            elapsed_ms,
        )
        return response