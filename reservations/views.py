from django.contrib import messages
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from reservations.forms import ContactForm, NewsletterForm, ReservationForm
from reservations.models import NewsletterSubscriber


def reserve(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save()
            d_str = reservation.date.strftime("%d.%m.%Y")
            t_str = reservation.time.strftime("%H:%M")
            t_info = f" (Стіл №{reservation.table_number})" if reservation.table_number else ""
            messages.success(
                request,
                f"Дякуємо, {reservation.name}! Бронювання на {d_str} о {t_str}{t_info} прийнято. "
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


@require_POST
def newsletter_subscribe(request: HttpRequest) -> HttpResponse:
    is_ajax = (
        request.headers.get("x-requested-with") == "XMLHttpRequest"
        or "application/json" in request.headers.get("Accept", "")
    )
    email = request.POST.get("email", "").strip().lower()
    form = NewsletterForm({"email": email})

    if form.is_valid():
        _, created = NewsletterSubscriber.objects.get_or_create(email=email)
        if created:
            msg = "Дякуємо за підписку! Ви успішно приєдналися до спільноти Savoure Privilège."
            status_type = "success"
        else:
            msg = "Цей email уже підписаний на розсилку Savoure."
            status_type = "info"

        if is_ajax:
            return JsonResponse({"status": status_type, "message": msg})
        if status_type == "success":
            messages.success(request, msg)
        else:
            messages.info(request, msg)
    else:
        if email and NewsletterSubscriber.objects.filter(email=email).exists():
            msg = "Цей email уже підписаний на розсилку Savoure."
            if is_ajax:
                return JsonResponse({"status": "info", "message": msg})
            messages.info(request, msg)
        else:
            msg = "Будь ласка, введіть коректну адресу електронної пошти."
            if is_ajax:
                return JsonResponse({"status": "error", "message": msg}, status=400)
            messages.error(request, msg)

    referer = request.META.get("HTTP_REFERER")
    if referer:
        return HttpResponseRedirect(referer)
    return redirect(reverse("core:home"))
