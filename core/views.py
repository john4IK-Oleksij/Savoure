from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from blog.models import BlogPost
from menu.models import Dish
from reservations.forms import ContactForm


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
