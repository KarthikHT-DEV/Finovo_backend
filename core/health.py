"""
Health check endpoint for ALB / Target Group.

Returns 200 OK when the app and database are healthy.
Returns 503 Service Unavailable if the database is unreachable.
"""
import logging

from django.db import connection
from django.http import JsonResponse

logger = logging.getLogger(__name__)


def health_check(request):
    """
    Lightweight health probe used by the ALB target group.

    • Verifies the Django process is alive.
    • Runs a trivial ``SELECT 1`` against PostgreSQL (RDS) to confirm
      database connectivity.
    • No authentication required — the ALB calls this directly.
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        return JsonResponse({"status": "ok", "database": "connected"})
    except Exception as exc:
        logger.error("Health check failed — database unreachable: %s", exc)
        return JsonResponse(
            {"status": "error", "database": str(exc)},
            status=503,
        )
