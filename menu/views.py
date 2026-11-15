from typing import Any

from django.db.models import Prefetch
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render

from menu.models import Category, Dish


def dish_list(request: HttpRequest) -> HttpResponse:
    available_dishes_prefetch = Prefetch(
        "dishes",
        queryset=Dish.objects.filter(is_available=True).prefetch_related("tags"),
    )
    categories = (
        Category.objects.all()
        .prefetch_related(available_dishes_prefetch)
        .order_by("order", "name")
    )
    all_dishes = (
        Dish.objects.filter(is_available=True)
        .select_related("category")
        .prefetch_related("tags")
    )

    context: dict[str, Any] = {
        "active_nav": "menu",
        "categories": categories,
        "all_dishes": all_dishes,
    }
    return render(request, "menu/our-menu.html", context)


def api_dishes(request: HttpRequest) -> JsonResponse:
    category_slug = request.GET.get("category")
    dishes_qs = Dish.objects.filter(is_available=True).select_related("category")
    if category_slug and category_slug != "all":
        dishes_qs = dishes_qs.filter(category__slug=category_slug)

    data: list[dict[str, Any]] = [
        {
            "id": dish.id,
            "title": dish.title,
            "slug": dish.slug,
            "category": dish.category.slug,
            "category_name": dish.category.name,
            "price": str(dish.price),
            "description": dish.description,
            "image": dish.image.url if dish.image else "",
            "is_chef_special": dish.is_chef_special,
        }
        for dish in dishes_qs
    ]
    return JsonResponse({"dishes": data})
