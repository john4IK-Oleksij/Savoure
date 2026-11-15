from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest
from django.utils.html import format_html
from django.utils.safestring import SafeString, mark_safe

from reservations.models import ContactMessage, NewsletterSubscriber, Reservation


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin[Reservation]):
    list_display = (
        "name",
        "phone",
        "display_date",
        "display_time",
        "guests",
        "table_number",
        "display_special_request",
        "status",
        "display_created_at",
    )
    list_editable = ("status", "table_number")
    list_filter = ("status", "table_number", "date")
    search_fields = ("name", "phone", "email", "special_request")
    readonly_fields = ("created_at", "updated_at")
    actions = (
        "confirm_reservations",
        "cancel_reservations",
        "complete_reservations",
    )

    fieldsets = (
        ("Гість та контакти", {"fields": ("name", "phone", "email")}),
        (
            "Деталі візиту",
            {"fields": ("date", "time", "guests", "table_number")},
        ),
        ("Статус та побажання", {"fields": ("status", "special_request")}),
        (
            "Службова інформація",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    @admin.display(ordering="date", description="Дата")
    def display_date(self, obj: Reservation) -> str:
        return obj.date.strftime("%d.%m.%Y")

    @admin.display(ordering="time", description="Час")
    def display_time(self, obj: Reservation) -> str:
        return obj.time.strftime("%H:%M")

    @admin.display(ordering="created_at", description="Створено")
    def display_created_at(self, obj: Reservation) -> str:
        return obj.created_at.strftime("%d.%m.%Y %H:%M")

    @admin.display(description="Побажання / Подія")
    def display_special_request(self, obj: Reservation) -> SafeString:
        if not obj.special_request or not obj.special_request.strip():
            return mark_safe('<span style="color:#64748b;">—</span>')

        req = obj.special_request.strip()
        req_lower = req.lower()

        if any(w in req_lower for w in ["wedding", "весіл", "anniversary", "річниц"]):
            icon = "🥂 "
            color = "#f5d372"
            bg = "rgba(245, 211, 114, 0.16)"
            border = "rgba(245, 211, 114, 0.6)"
        elif any(w in req_lower for w in ["birthday", "народжен", "b-day"]):
            icon = "🎂 "
            color = "#f472b6"
            bg = "rgba(244, 114, 182, 0.16)"
            border = "rgba(244, 114, 182, 0.6)"
        elif any(w in req_lower for w in ["allerg", "алерг"]):
            icon = "⚠️ "
            color = "#ef4444"
            bg = "rgba(239, 68, 68, 0.16)"
            border = "rgba(239, 68, 68, 0.6)"
        elif any(w in req_lower for w in ["romantic", "побачен", "love"]):
            icon = "🌹 "
            color = "#fb7185"
            bg = "rgba(251, 113, 133, 0.16)"
            border = "rgba(251, 113, 133, 0.6)"
        else:
            icon = "💬 "
            color = "#38bdf8"
            bg = "rgba(56, 189, 248, 0.14)"
            border = "rgba(56, 189, 248, 0.5)"

        short_text = req if len(req) <= 26 else f"{req[:23]}..."
        return format_html(
            '<span title="{}" style="display:inline-flex;align-items:center;padding:2px 8px;'
            'border-radius:10px;background:{};color:{};font-size:11px;font-weight:600;'
            'border:1px solid {};white-space:nowrap;cursor:help;">{}{}'
            '</span>',
            req,
            bg,
            color,
            border,
            icon,
            short_text,
        )

    @admin.action(description="Підтвердити обрані бронювання")
    def confirm_reservations(
        self,
        request: HttpRequest,
        queryset: QuerySet[Reservation],
    ) -> None:
        count = queryset.update(status=Reservation.Status.CONFIRMED)
        self.message_user(request, f"Підтверджено бронювань: {count}")

    @admin.action(description="Скасувати обрані бронювання")
    def cancel_reservations(
        self,
        request: HttpRequest,
        queryset: QuerySet[Reservation],
    ) -> None:
        count = queryset.update(status=Reservation.Status.CANCELLED)
        self.message_user(request, f"Скасовано бронювань: {count}")

    @admin.action(description="Позначити як виконані (візит завершено)")
    def complete_reservations(
        self,
        request: HttpRequest,
        queryset: QuerySet[Reservation],
    ) -> None:
        count = queryset.update(status=Reservation.Status.COMPLETED)
        self.message_user(request, f"Позначено як виконані: {count}")


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin[ContactMessage]):
    list_display = ("name", "email", "phone", "is_processed", "created_at")
    list_editable = ("is_processed",)
    list_filter = ("is_processed", "created_at")
    search_fields = ("name", "email", "message")
    readonly_fields = ("created_at",)


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin[NewsletterSubscriber]):
    list_display = ("email", "subscribed_at")
    search_fields = ("email",)
    readonly_fields = ("subscribed_at",)
