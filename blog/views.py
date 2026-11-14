from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def blog_list(request: HttpRequest) -> HttpResponse:
    return render(request, "blog/blog.html", {"active_nav": "news"})


def blog_detail(request: HttpRequest, slug: str) -> HttpResponse:
    return render(request, "blog/detail.html", {"active_nav": "news", "slug": slug})
