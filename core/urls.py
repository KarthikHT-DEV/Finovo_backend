from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from core.health import health_check

urlpatterns = [
    path("admin/", admin.site.urls),

    # ALB health check — no auth required
    path("api/health/", health_check, name="health-check"),

    # App routes
    path("api/auth/", include("users.urls")),
    path("api/transactions/", include("transactions.urls")),

    # Generic api routes
    path("api/", include("core.api_urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
