import json
import shutil
from decimal import Decimal
from typing import Any

from django.conf import settings
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from blog.models import BlogPost
from menu.models import Category, Dish
from reservations.models import ContactMessage, NewsletterSubscriber, Reservation


class Command(BaseCommand):
    help = (
        "Initializes Savoure database: sets up RBAC permission groups (Chef & Manager) "
        "and seeds initial menu/blog data. Does NOT create users or store credentials."
    )

    def handle(self, *args: Any, **options: Any) -> None:
        self.stdout.write(self.style.NOTICE("🚀 Starting Savoure initial setup..."))

        self._setup_roles()
        self._seed_menu_data()
        self._seed_blog_data()

        self.stdout.write(self.style.SUCCESS("✨ Setup completed successfully!"))

    def _setup_roles(self) -> None:
        self.stdout.write("👤 Setting up RBAC permission groups (Chef & Manager)...")

        # 1. Chef Group
        chef_group, _ = Group.objects.get_or_create(name="Chef")
        menu_ct = ContentType.objects.get_for_model(Dish)
        cat_ct = ContentType.objects.get_for_model(Category)
        chef_perms = Permission.objects.filter(content_type__in=[menu_ct, cat_ct])
        chef_group.permissions.set(chef_perms)
        self.stdout.write(self.style.SUCCESS("  [+] Chef group permissions configured."))

        # 2. Manager Group
        manager_group, _ = Group.objects.get_or_create(name="Manager")
        res_ct = ContentType.objects.get_for_model(Reservation)
        msg_ct = ContentType.objects.get_for_model(ContactMessage)
        sub_ct = ContentType.objects.get_for_model(NewsletterSubscriber)
        manager_perms = Permission.objects.filter(content_type__in=[res_ct, msg_ct, sub_ct])
        manager_group.permissions.set(manager_perms)
        self.stdout.write(self.style.SUCCESS("  [+] Manager group permissions configured."))

    def _seed_menu_data(self) -> None:
        self.stdout.write("🍽️  Seeding Categories and Dishes...")
        menu_file = settings.BASE_DIR / "static" / "data" / "menu.json"
        if not menu_file.exists():
            self.stdout.write(self.style.WARNING("  [!] static/data/menu.json not found."))
            return

        with menu_file.open("r", encoding="utf-8") as f:
            data = json.load(f)

        # Ensure media directory exists
        media_dishes_dir = settings.MEDIA_ROOT / "dishes"
        media_dishes_dir.mkdir(parents=True, exist_ok=True)

        categories_map = {
            "appetizer": ("Закуски (Appetizers)", 10),
            "main": ("Основні страви (Main Course)", 20),
            "dessert": ("Десерти (Desserts)", 30),
            "beverage": ("Напої (Beverages)", 40),
        }

        created_categories: dict[str, Category] = {}
        for slug, (name, order) in categories_map.items():
            cat_obj, _ = Category.objects.get_or_create(
                slug=slug,
                defaults={"name": name, "order": order},
            )
            created_categories[slug] = cat_obj

        dishes_count = 0
        for item in data:
            title = item.get("title", "").strip()
            cat_key = item.get("category", "main")
            category_obj = created_categories.get(cat_key)

            slug = slugify(title)
            if not slug:
                continue

            raw_price = Decimal(str(item.get("price", 10)))
            featured = bool(item.get("featured", False))
            desc = item.get("description", "")
            img_rel = item.get("image", "").lstrip("/")

            # Copy image to media/dishes if exists in static
            media_img_path = ""
            if img_rel:
                static_img = settings.BASE_DIR / "static" / img_rel
                if static_img.exists():
                    target_img = media_dishes_dir / static_img.name
                    if not target_img.exists():
                        shutil.copyfile(static_img, target_img)
                    media_img_path = f"dishes/{static_img.name}"

            _, created = Dish.objects.get_or_create(
                slug=slug,
                defaults={
                    "title": title,
                    "category": category_obj,
                    "price": raw_price,
                    "description": desc,
                    "is_available": True,
                    "is_chef_special": featured,
                    "image": media_img_path,
                },
            )
            if created:
                dishes_count += 1

        self.stdout.write(self.style.SUCCESS(f"  [+] Added {dishes_count} new dishes to menu."))

    def _seed_blog_data(self) -> None:
        self.stdout.write("📰 Seeding Blog Posts...")
        blog_file = settings.BASE_DIR / "static" / "data" / "blog.json"
        if not blog_file.exists():
            return

        with blog_file.open("r", encoding="utf-8") as f:
            data = json.load(f)

        media_blog_dir = settings.MEDIA_ROOT / "blog"
        media_blog_dir.mkdir(parents=True, exist_ok=True)

        posts_count = 0
        for item in data:
            slug = item.get("slug") or slugify(item.get("title", ""))
            if not slug or BlogPost.objects.filter(slug=slug).exists():
                continue

            img_rel = item.get("image", "").lstrip("/")
            media_img_path = ""
            if img_rel:
                static_img = settings.BASE_DIR / "static" / img_rel
                if static_img.exists():
                    target_img = media_blog_dir / static_img.name
                    if not target_img.exists():
                        shutil.copyfile(static_img, target_img)
                    media_img_path = f"blog/{static_img.name}"

            BlogPost.objects.create(
                title=item.get("title", ""),
                slug=slug,
                description=item.get("description", ""),
                content=item.get("description", ""),
                published_at=item.get("date", "2026-05-01"),
                is_published=True,
                image=media_img_path,
            )
            posts_count += 1

        self.stdout.write(self.style.SUCCESS(f"  [+] Added {posts_count} blog posts."))
