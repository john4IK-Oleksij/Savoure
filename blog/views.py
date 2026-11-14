from typing import Any

from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render

from blog.models import BlogPost


def blog_list(request: HttpRequest) -> HttpResponse:
    posts_list = BlogPost.objects.filter(is_published=True).order_by(
        "-published_at",
        "-created_at",
    )
    paginator = Paginator(posts_list, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context: dict[str, Any] = {
        "active_nav": "news",
        "page_obj": page_obj,
        "posts": page_obj.object_list,
    }
    return render(request, "blog/blog.html", context)


def blog_detail(request: HttpRequest, slug: str) -> HttpResponse:
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    recent_posts = BlogPost.objects.filter(is_published=True).exclude(id=post.id)[:3]

    context: dict[str, Any] = {
        "active_nav": "news",
        "post": post,
        "recent_posts": recent_posts,
    }
    return render(request, "blog/detail.html", context)
