from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def dish_list(request: HttpRequest) -> HttpResponse:
    return render(request, "menu/our-menu.html", {"active_nav": "menu"})
