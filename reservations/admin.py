from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest

from reservations.models import ContactMessage, NewsletterSubscriber, Reservation


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "phone",
        "email",
        "date",
        "time",
        "guests",
        "status",
        "created_at",
    )
    list_editable = ("status",)
    list_filter = ("status", "date")
    search_fields = ("name", "phone", "email")
    readonly_fields = ("created_at", "updated_at")
    actions = ("confirm_reservations", "cancel_reservations")

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


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "is_processed", "created_at")
    list_editable = ("is_processed",)
    list_filter = ("is_processed", "created_at")
    search_fields = ("name", "email", "message")
    readonly_fields = ("created_at",)


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ("email", "subscribed_at")
    search_fields = ("email",)
    readonly_fields = ("subscribed_at",)
