"""
Middleware to log every HTTP request to requests.log.
"""
import logging

logger = logging.getLogger("request_log")


class RequestLoggingMiddleware:
    """Log each request method, path, and response status to request_log (writes to requests.log)."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        try:
            logger.info(
                "%s %s -> %s",
                request.method,
                request.path,
                getattr(response, "status_code", "?"),
            )
        except Exception:
            pass
        return response
