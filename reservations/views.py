from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def reserve(request: HttpRequest) -> HttpResponse:
    return render(request, "reservations/reservation.html", {"active_nav": ""})
