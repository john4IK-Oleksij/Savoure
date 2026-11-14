from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField("Назва категорії", max_length=100, unique=True)
    slug = models.SlugField("Slug", max_length=100, unique=True)
    order = models.PositiveIntegerField("Порядок сортування", default=0)

    class Meta:
        verbose_name = "категорія"
        verbose_name_plural = "категорії"
        ordering = ("order", "name")

    def __str__(self) -> str:
        return self.name


class Tag(models.Model):
    name = models.CharField("Назва тегу", max_length=50, unique=True)
    badge_color = models.CharField(
        "Колір бейджа (CSS/HEX)",
        max_length=20,
        default="#f4c73f",
    )

    class Meta:
        verbose_name = "тег"
        verbose_name_plural = "теги"
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name


class Dish(models.Model):
    class Spiciness(models.IntegerChoices):
        NONE = 0, "Без гостроти"
        MILD = 1, "Пікантне"
        HOT = 2, "Гостре"

    title = models.CharField("Назва страви", max_length=200)
    slug = models.SlugField("Slug", max_length=200, unique=True)
    description = models.TextField("Опис", blank=True)
    price = models.DecimalField(
        "Ціна ($)",
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    weight_grams = models.PositiveIntegerField("Вага, г", default=250)
    spiciness = models.PositiveSmallIntegerField(
        "Гострота",
        choices=Spiciness.choices,
        default=Spiciness.NONE,
    )
    is_available = models.BooleanField("У наявності", default=True)
    is_chef_special = models.BooleanField("Шеф-рекомендація", default=False)
    image = models.ImageField(
        "Фотографія страви",
        upload_to="dishes/%Y/%m/",
        blank=True,
        null=True,
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="dishes",
        verbose_name="Категорія",
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name="dishes",
        verbose_name="Теги / Особливості",
    )

    created_at = models.DateTimeField("Створено", auto_now_add=True)
    updated_at = models.DateTimeField("Оновлено", auto_now=True)

    class Meta:
        verbose_name = "страва"
        verbose_name_plural = "страви"
        ordering = ("-is_chef_special", "category", "title")

    def __str__(self) -> str:
        return f"{self.title} (${self.price})"

    def get_absolute_url(self) -> str:
        return reverse("menu:dish_list")
