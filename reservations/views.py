from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from reservations.forms import ContactForm, NewsletterForm, ReservationForm


def reserve(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save()
            d_str = reservation.date.strftime("%d.%m.%Y")
            t_str = reservation.time.strftime("%H:%M")
            messages.success(
                request,
                f"Дякуємо, {reservation.name}! Ваше бронювання на {d_str} о {t_str} прийнято. "
                "Менеджер ресторану зателефонує вам для підтвердження.",
            )
            return redirect("reservations:reserve")
        else:
            messages.error(
                request,
                "Будь ласка, перевірте правильність заповнення полів форми бронювання.",
            )
    else:
        form = ReservationForm()

    return render(
        request,
        "reservations/reservation.html",
        {"form": form, "active_nav": ""},
    )


def contact_submit(request: HttpRequest) -> HttpResponseRedirect:
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Ваше повідомлення успішно надіслано! Ми зв'яжемося з вами найближчим часом.",
            )
        else:
            messages.error(
                request,
                "Помилка при відправці форми. Перевірте правильність введених даних.",
            )

    referer = request.META.get("HTTP_REFERER")
    if referer:
        return HttpResponseRedirect(referer)
    return redirect("core:home")


def newsletter_subscribe(request: HttpRequest) -> HttpResponseRedirect:
    if request.method == "POST":
        form = NewsletterForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Дякуємо за підписку на новини ресторану Savoure!")
            except IntegrityError:
                messages.info(request, "Цей email уже підписаний на наші новини.")
        else:
            messages.error(request, "Введіть коректну адресу електронної пошти.")

    referer = request.META.get("HTTP_REFERER")
    if referer:
        return HttpResponseRedirect(referer)
    return redirect(reverse("core:home"))
