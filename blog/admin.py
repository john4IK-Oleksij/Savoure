from django.contrib import admin

from blog.models import BlogPost


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "published_at", "is_published", "created_at")
    list_editable = ("is_published",)
    list_filter = ("is_published", "published_at")
    search_fields = ("title", "description", "content")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("created_at", "updated_at")
