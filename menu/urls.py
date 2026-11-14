from django.urls import path

from menu import views

app_name = "menu"

urlpatterns = [
    path("", views.dish_list, name="dish_list"),
    path("api/dishes/", views.api_dishes, name="api_dishes"),
]
