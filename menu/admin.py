from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest
from django.utils.html import format_html
from django.utils.safestring import SafeString

from menu.models import Category, Dish, Tag


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin[Category]):
    list_display = ("order", "name", "slug")
    list_display_links = ("name",)
    list_editable = ("order",)
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin[Tag]):
    list_display = ("name", "badge_color")
    search_fields = ("name",)


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin[Dish]):
    list_display = (
        "title",
        "category",
        "price",
        "weight_grams",
        "is_available",
        "is_chef_special",
        "display_tags",
        "display_image",
    )
    list_editable = ("price", "is_available", "is_chef_special")
    list_filter = ("is_available", "is_chef_special", "category", "tags")
    search_fields = ("title", "description", "category__name")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("tags",)
    readonly_fields = ("created_at", "updated_at")
    actions = ("make_available", "make_unavailable")

    fieldsets = (
        (None, {"fields": ("title", "slug", "category", "description", "image")}),
        ("Характеристики та ціна", {"fields": ("price", "weight_grams", "spiciness")}),
        ("Маркетинг та статус", {"fields": ("is_available", "is_chef_special", "tags")}),
        (
            "Службова інформація",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    @admin.display(description="Теги")
    def display_tags(self, obj: Dish) -> SafeString:
        tags = obj.tags.all()
        if not tags:
            return format_html('<span style="color:#718096;">—</span>')
        badges = [
            (
                f'<span style="background:{t.badge_color}22;border:1px solid {t.badge_color};'
                f'color:{t.badge_color};padding:2px 8px;border-radius:10px;'
                f'font-size:11px;font-weight:600;">{t.name}</span>'
            )
            for t in tags
        ]
        return format_html(" ".join(badges))

    @admin.display(description="Мініатюра")
    def display_image(self, obj: Dish) -> SafeString | str:
        if obj.image:
            return format_html(
                '<img src="{}" style="height:45px;width:45px;'
                'border-radius:6px;object-fit:cover;" />',
                obj.image.url,
            )
        return "—"

    @admin.action(description="Позначити як доступні")
    def make_available(self, request: HttpRequest, queryset: QuerySet[Dish]) -> None:
        count = queryset.update(is_available=True)
        self.message_user(request, f"Оновлено страв у меню: {count}")

    @admin.action(description="Зняти з меню (поставити на стоп)")
    def make_unavailable(self, request: HttpRequest, queryset: QuerySet[Dish]) -> None:
        count = queryset.update(is_available=False)
        self.message_user(request, f"Поставлено на стоп страв: {count}")
