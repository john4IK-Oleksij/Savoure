from django.db import models


class Reservation(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Очікує підтвердження"
        CONFIRMED = "confirmed", "Підтверджено"
        CANCELLED = "cancelled", "Скасовано"
        COMPLETED = "completed", "Виконано"

    name = models.CharField("Ім'я гостя", max_length=150)
    email = models.EmailField("Email")
    phone = models.CharField("Номер телефону", max_length=30)
    date = models.DateField("Дата візиту")
    time = models.TimeField("Час візиту")
    guests = models.PositiveSmallIntegerField("Кількість гостей", default=2)
    special_request = models.TextField("Особливі побажання", blank=True)
    status = models.CharField(
        "Статус бронювання",
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )

    created_at = models.DateTimeField("Створено", auto_now_add=True)
    updated_at = models.DateTimeField("Оновлено", auto_now=True)

    class Meta:
        verbose_name = "бронювання"
        verbose_name_plural = "бронювання"
        ordering = ("-date", "-time")

    def __str__(self) -> str:
        return f"Бронь: {self.name} — {self.date} {self.time} ({self.get_status_display()})"


class ContactMessage(models.Model):
    name = models.CharField("Ім'я", max_length=150)
    email = models.EmailField("Email")
    phone = models.CharField("Номер телефону", max_length=30, blank=True)
    message = models.TextField("Повідомлення")
    is_processed = models.BooleanField("Опрацьовано", default=False)
    created_at = models.DateTimeField("Надіслано", auto_now_add=True)

    class Meta:
        verbose_name = "контактне повідомлення"
        verbose_name_plural = "контактні повідомлення"
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return f"{self.name} ({self.email}) — {self.created_at.strftime('%d.%m.%Y %H:%M')}"


class NewsletterSubscriber(models.Model):
    email = models.EmailField("Email підписника", unique=True)
    subscribed_at = models.DateTimeField("Дата підписки", auto_now_add=True)

    class Meta:
        verbose_name = "підписник розсилки"
        verbose_name_plural = "підписники розсилки"
        ordering = ("-subscribed_at",)

    def __str__(self) -> str:
        return self.email
