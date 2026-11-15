"""
Main URL configuration for Savoure Restaurant.
"""

import sys
import traceback

from django.contrib import admin
from django.http import HttpRequest, HttpResponse
from django.urls import include, path, re_path
from django.views.generic.base import RedirectView

from core.views import serve_media_with_fallback

admin.site.site_header = "SAVOURE Backstage"
admin.site.site_title = "SAVOURE Backstage"
admin.site.index_title = "Панель керування рестораном"


def custom_server_error(request: HttpRequest) -> HttpResponse:
    exc_type, exc_val, exc_tb = sys.exc_info()
    tb_text = "".join(traceback.format_exception(exc_type, exc_val, exc_tb))
    print(f"=== DJANGO 500 ERROR ON {request.path} ===\n{tb_text}", flush=True)
    return HttpResponse(
        f"<!DOCTYPE html><html><head><title>500 Error Details</title></head>"
        f"<body style='background:#0f172a;color:#f87171;font-family:monospace;padding:24px;'>"
        f"<h2 style='color:#f5d372;'>SAVOURE Backstage — Server Error (500)</h2>"
        f"<p style='color:#cbd5e1;'>Path: {request.path}</p>"
        f"<pre style='background:#1e293b;padding:16px;border-radius:8px;"
        f"overflow:auto;color:#fca5a5;'>{tb_text}</pre>"
        f"</body></html>",
        status=500,
        content_type="text/html",
    )


handler500 = custom_server_error

urlpatterns = [
    # Global favicon for whole domain and all admin pages (Eiffel tower)
    path("favicon.ico", RedirectView.as_view(url="/static/assets/img/favicon.ico", permanent=True)),
    path("backstage/", admin.site.urls),
    path("", include("core.urls", namespace="core")),
    path("menu/", include("menu.urls", namespace="menu")),
    path("reservations/", include("reservations.urls", namespace="reservations")),
    path("news/", include("blog.urls", namespace="blog")),
    # Serve user & admin uploaded media files with automatic fallback to built-in assets
    re_path(r"^media/(?P<path>.*)$", serve_media_with_fallback),
]

