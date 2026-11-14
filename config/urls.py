"""
Main URL configuration for Savoure Restaurant.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path("admin/", admin.site.urls),
    # Local apps will be included here as we build them:
    # path("", include("core.urls", namespace="core")),
    # path("menu/", include("menu.urls", namespace="menu")),
    # path("reservations/", include("reservations.urls", namespace="reservations")),
    # path("news/", include("blog.urls", namespace="blog")),
]

# Serve media files during local development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
