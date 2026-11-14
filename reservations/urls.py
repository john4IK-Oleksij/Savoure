from django.urls import path

from reservations import views

app_name = "reservations"

urlpatterns = [
    path("", views.reserve, name="reserve"),
]
