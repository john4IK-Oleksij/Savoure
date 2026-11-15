from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest
from django.utils.html import format_html
from django.utils.safestring import SafeString, mark_safe

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
    list_display = ("name", "badge_color", "display_preview")
    list_editable = ("badge_color",)
    search_fields = ("name",)

    @admin.display(description="Попередній перегляд")
    def display_preview(self, obj: Tag) -> SafeString:
        return format_html(
            '<span style="display:inline-block;padding:2px 10px;border-radius:12px;'
            'background:rgba(255,255,255,0.08);color:{};font-weight:600;'
            'border:1px solid {};">{}</span>',
            obj.badge_color,
            obj.badge_color,
            obj.name,
        )


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin[Dish]):
    list_display = (
        "title",
        "category",
        "price",
        "weight_grams",
        "display_spiciness",
        "is_available",
        "is_chef_special",
        "display_tags",
        "display_image",
    )
    list_editable = ("price", "is_available", "is_chef_special")
    list_filter = ("is_available", "is_chef_special", "category", "tags")
    search_fields = ("title", "description", "category__name")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("created_at", "updated_at")

    def get_queryset(self, request: HttpRequest) -> QuerySet[Dish]:
        return super().get_queryset(request).prefetch_related("tags", "category")

    fieldsets = (
        (None, {"fields": ("title", "slug", "category", "description", "image")}),
        ("Характеристики та ціна", {"fields": ("price", "weight_grams", "spiciness")}),
        ("Маркетинг та статус", {"fields": ("is_available", "is_chef_special", "tags")}),
        (
            "Службова інформація",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    @admin.display(description="Гострота")
    def display_spiciness(self, obj: Dish) -> str:
        if obj.spiciness == 1:
            return "🌶️"
        if obj.spiciness == 2:
            return "🌶️🌶️"
        return "—"

    @admin.display(description="Теги")
    def display_tags(self, obj: Dish) -> SafeString:
        tags: list[Tag] = list(obj.tags.all())
        if not tags:
            return mark_safe('<span style="color:#718096;">—</span>')
        badges: list[str] = [
            f'<span style="color:{t.badge_color};font-weight:600;">{t.name}</span>'
            for t in tags
        ]
        return mark_safe(", ".join(badges))

    @admin.display(description="Мініатюра")
    def display_image(self, obj: Dish) -> SafeString | str:
        if obj.image:
            return format_html(
                '<img src="{}" style="height:45px;width:45px;'
                'border-radius:6px;object-fit:cover;" />',
                obj.image.url,
            )
        return "—"
