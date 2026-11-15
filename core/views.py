from pathlib import Path

from django.conf import settings
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.static import serve

from blog.models import BlogPost
from menu.models import Dish
from reservations.forms import ContactForm


def serve_media_with_fallback(request: HttpRequest, path: str) -> HttpResponse:
    """
    Serves media files with fallback to built-in static dish assets.
    Guarantees that uploaded dish images never 404 even across ephemeral container redeploys.
    """
    media_file: Path = settings.MEDIA_ROOT / path
    if media_file.exists():
        return serve(request, path, document_root=settings.MEDIA_ROOT)

    filename: str = Path(path).name
    static_dish_dir: Path = settings.BASE_DIR / "static" / "dish-list"
    if (static_dish_dir / filename).exists():
        return serve(request, filename, document_root=static_dish_dir)

    raise Http404("Media file not found")


def home(request: HttpRequest) -> HttpResponse:
    chef_favorites = (
        Dish.objects.filter(is_available=True, is_chef_special=True)
        .select_related("category")
        .prefetch_related("tags")[:6]
    )
    latest_posts = BlogPost.objects.filter(is_published=True)[:3]
    contact_form = ContactForm()

    return render(
        request,
        "core/index.html",
        {
            "active_nav": "home",
            "chef_favorites": chef_favorites,
            "latest_posts": latest_posts,
            "contact_form": contact_form,
        },
    )


def about(request: HttpRequest) -> HttpResponse:
    return render(request, "core/about.html", {"active_nav": "about"})


def findus(request: HttpRequest) -> HttpResponse:
    contact_form = ContactForm()
    return render(
        request,
        "core/findus.html",
        {"active_nav": "location", "contact_form": contact_form},
    )


def privacy(request: HttpRequest) -> HttpResponse:
    return render(request, "core/privacy.html", {"active_nav": ""})


def terms(request: HttpRequest) -> HttpResponse:
    return render(request, "core/terms.html", {"active_nav": ""})
