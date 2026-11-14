from datetime import date, datetime, timezone
from typing import Any

from django import forms

from reservations.models import ContactMessage, NewsletterSubscriber, Reservation


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ("name", "email", "phone", "date", "time", "guests", "special_request")
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form__input",
                    "placeholder": "Input your name",
                    "required": "required",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form__input",
                    "placeholder": "example@email.com",
                    "required": "required",
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "class": "form__input",
                    "placeholder": "+1 234 567 890",
                    "required": "required",
                }
            ),
            "date": forms.DateInput(
                attrs={
                    "class": "form__input",
                    "type": "date",
                    "required": "required",
                }
            ),
            "time": forms.TimeInput(
                attrs={
                    "class": "form__input",
                    "type": "time",
                    "required": "required",
                }
            ),
            "guests": forms.NumberInput(
                attrs={
                    "class": "form__input",
                    "min": "1",
                    "max": "20",
                    "value": "2",
                    "required": "required",
                }
            ),
            "special_request": forms.Textarea(
                attrs={
                    "class": "form__input form__textarea",
                    "placeholder": "Special dietary requests, table preferences...",
                    "rows": "4",
                }
            ),
        }

    def clean_date(self) -> date:
        reservation_date = self.cleaned_data.get("date")
        if not reservation_date:
            raise forms.ValidationError("Будь ласка, вкажіть дату бронювання.")
        today = datetime.now(timezone.utc).date()
        if reservation_date < today:
            raise forms.ValidationError("Дата бронювання не може бути в минулому.")
        return reservation_date

    def clean_guests(self) -> int:
        guests: Any = self.cleaned_data.get("guests")
        if not guests or int(guests) < 1:
            raise forms.ValidationError("Кількість гостей повинна бути не менше 1.")
        if int(guests) > 20:
            raise forms.ValidationError(
                "Для бронювання понад 20 гостей, будь ласка, зателефонуйте нам напряму."
            )
        return int(guests)


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ("name", "email", "phone", "message")
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "contact-form__input",
                    "placeholder": "Input text here",
                    "required": "required",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "contact-form__input",
                    "placeholder": "Input text here",
                    "required": "required",
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "class": "contact-form__input",
                    "placeholder": "+1 234 567 890",
                }
            ),
            "message": forms.Textarea(
                attrs={
                    "class": "contact-form__input contact-form__textarea",
                    "placeholder": "Input text here",
                    "rows": "4",
                    "required": "required",
                }
            ),
        }


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscriber
        fields = ("email",)
        widgets = {
            "email": forms.EmailInput(
                attrs={
                    "class": "footer__subscribe-input",
                    "placeholder": "Enter your email address",
                    "required": "required",
                }
            ),
        }
