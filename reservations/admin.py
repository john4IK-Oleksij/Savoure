from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest

from reservations.models import ContactMessage, NewsletterSubscriber, Reservation


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin[Reservation]):
    list_display = (
        "name",
        "phone",
        "date",
        "time",
        "guests",
        "table_number",
        "status",
        "created_at",
    )
    list_editable = ("status", "table_number")
    list_filter = ("status", "table_number", "date")
    search_fields = ("name", "phone", "email")
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
