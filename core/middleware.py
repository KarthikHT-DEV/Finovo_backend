"""
Middleware to allow ALB health checks regardless of Host header.

ALB health checkers send requests with Host: <private-ip>:8000 instead of
the ALB DNS name. This middleware bypasses Django's ALLOWED_HOSTS check
for the health endpoint only.
"""
from django.http import JsonResponse
from django.db import connection


class HealthCheckMiddleware:
    """
    Intercepts GET /api/health/ BEFORE Django's CommonMiddleware runs
    the ALLOWED_HOSTS check, so ALB probes always get a valid response.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == "/api/health/":
            try:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT 1")
                return JsonResponse({"status": "ok", "database": "connected"})
            except Exception as exc:
                return JsonResponse(
                    {"status": "error", "database": str(exc)},
                    status=503,
                )
        return self.get_response(request)
