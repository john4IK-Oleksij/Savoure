"""
Main URL configuration for Savoure Restaurant.
"""

from django.contrib import admin
from django.urls import include, path, re_path

from core.views import serve_media_with_fallback

urlpatterns = [
    path("backstage/", admin.site.urls),
    path("", include("core.urls", namespace="core")),
    path("menu/", include("menu.urls", namespace="menu")),
    path("reservations/", include("reservations.urls", namespace="reservations")),
    path("news/", include("blog.urls", namespace="blog")),
    # Serve user & admin uploaded media files with automatic fallback to built-in assets
    re_path(r"^media/(?P<path>.*)$", serve_media_with_fallback),
]

