from django.db import models
from django.urls import reverse


class BlogPost(models.Model):
    title = models.CharField("Заголовок статті", max_length=250)
    slug = models.SlugField("Slug", max_length=250, unique=True)
    image = models.ImageField(
        "Головне зображення",
        upload_to="blog/%Y/%m/",
        blank=True,
        null=True,
    )
    description = models.TextField("Короткий анонс / Опис", blank=True)
    content = models.TextField("Повний текст статті", blank=True)
    is_published = models.BooleanField("Опубліковано", default=True)
    published_at = models.DateField("Дата публікації")

    created_at = models.DateTimeField("Створено", auto_now_add=True)
    updated_at = models.DateTimeField("Оновлено", auto_now=True)

    class Meta:
        verbose_name = "стаття блогу"
        verbose_name_plural = "статті блогу"
        ordering = ("-published_at", "-created_at")

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self) -> str:
        return reverse("blog:blog_detail", kwargs={"slug": self.slug})
