from typing import Any
from django.db import migrations


def create_rbac_groups(apps: Any, schema_editor: Any) -> None:
    # Отримуємо історичні моделі через apps (щоб міграція працювала стабільно)
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")

    # 1. Створюємо групу Chef (Шеф-кухар)
    chef_group, _ = Group.objects.get_or_create(name="Chef")
    # Знаходимо всі дозволи для страв (dish) та категорій (category) меню
    chef_perms = Permission.objects.filter(
        content_type__app_label="menu",
        content_type__model__in=["dish", "category"],
    )
    chef_group.permissions.set(chef_perms)

    # 2. Створюємо групу Manager (Менеджер)
    manager_group, _ = Group.objects.get_or_create(name="Manager")
    # Знаходимо дозволи для бронювань, контактів та розсилки
    manager_perms = Permission.objects.filter(
        content_type__app_label="reservations",
        content_type__model__in=["reservation", "contactmessage", "newslettersubscriber"],
    )
    manager_group.permissions.set(manager_perms)


def remove_rbac_groups(apps: Any, schema_editor: Any) -> None:
    # Логіка відкату міграції (якщо колись знадобиться скасувати)
    Group = apps.get_model("auth", "Group")
    Group.objects.filter(name__in=["Chef", "Manager"]).delete()


class Migration(migrations.Migration):

    # Вказуємо залежності: ця міграція виконується ПІСЛЯ того, як створені моделі menu та reservations
    dependencies = [
        ("auth", "__latest__"),
        ("menu", "0001_initial"),
        ("reservations", "0001_initial"),
    ]

    operations = [
        # migrations.RunPython викликає нашу функцію під час python manage.py migrate
        migrations.RunPython(create_rbac_groups, reverse_code=remove_rbac_groups),
    ]