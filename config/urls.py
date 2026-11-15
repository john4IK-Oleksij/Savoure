"""
Main URL configuration for Savoure Restaurant.
"""

from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve

urlpatterns = [
    path("backstage/", admin.site.urls),
    path("", include("core.urls", namespace="core")),
    path("menu/", include("menu.urls", namespace="menu")),
    path("reservations/", include("reservations.urls", namespace="reservations")),
    path("news/", include("blog.urls", namespace="blog")),
    # Serve user & admin uploaded media files (dishes, blogs) in production and development
    re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
]

