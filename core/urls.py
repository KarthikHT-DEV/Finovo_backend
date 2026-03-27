from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    
    # Specific app routes first
    path("api/auth/", include("users.urls")),
    path("api/transactions/", include("transactions.urls")),
    
    # Generic api routes last
    path("api/", include("core.api_urls")),
    
    # Diagnostics (temporary)
    path("diagnostics-export/", include("transactions.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
