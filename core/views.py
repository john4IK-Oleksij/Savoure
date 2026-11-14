from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def home(request: HttpRequest) -> HttpResponse:
    return render(request, "core/index.html", {"active_nav": "home"})


def about(request: HttpRequest) -> HttpResponse:
    return render(request, "core/about.html", {"active_nav": "about"})


def findus(request: HttpRequest) -> HttpResponse:
    return render(request, "core/findus.html", {"active_nav": "location"})


def privacy(request: HttpRequest) -> HttpResponse:
    return render(request, "core/privacy.html", {"active_nav": ""})


def terms(request: HttpRequest) -> HttpResponse:
    return render(request, "core/terms.html", {"active_nav": ""})
