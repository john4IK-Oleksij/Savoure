from typing import Final

from django.contrib import admin, messages
from django.contrib.admin.actions import delete_selected as django_delete_selected
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.models import Group
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.utils.html import format_html
from django.utils.safestring import SafeString

PROTECTED_SYSTEM_GROUPS: Final[frozenset[str]] = frozenset({"Chef", "Manager"})


class CustomGroupAdmin(GroupAdmin):
    list_display = (
        "name",
        "display_group_type",
        "display_users_count",
        "display_permissions_count",
    )
    search_fields = ("name",)
    ordering = ("name",)
    actions = ("delete_selected",)

    def get_queryset(self, request: HttpRequest) -> QuerySet[Group]:
        return super().get_queryset(request).prefetch_related("user_set", "permissions")

    @admin.display(description="Тип ролі")
    def display_group_type(self, obj: Group) -> SafeString:
        if obj.name in PROTECTED_SYSTEM_GROUPS:
            return format_html(
                '<span style="display:inline-flex;align-items:center;padding:3px 10px;'
                'border-radius:10px;background:rgba(212,175,55,0.18);color:#f5d372;'
                'font-size:11px;font-weight:600;border:1px solid rgba(212,175,55,0.5);">'
                'Системна роль (захищена)'
                '</span>'
            )
        return format_html(
            '<span style="display:inline-flex;align-items:center;padding:3px 10px;'
            'border-radius:10px;background:rgba(100,116,139,0.16);color:#94a3b8;'
            'font-size:11px;font-weight:600;border:1px solid rgba(100,116,139,0.3);">'
            'Користувацька група'
            '</span>'
        )

    @admin.display(description="Користувачів у групі")
    def display_users_count(self, obj: Group) -> str:
        count = obj.user_set.count()
        return f"{count} користувач(ів)"

    @admin.display(description="Призначених прав")
    def display_permissions_count(self, obj: Group) -> str:
        count = obj.permissions.count()
        return f"{count} дозволів"

    def has_delete_permission(
        self,
        request: HttpRequest,
        obj: Group | None = None,
    ) -> bool:
        # Forbid deletion of protected system groups (Chef, Manager)
        if obj is not None and obj.name in PROTECTED_SYSTEM_GROUPS:
            return False
        return super().has_delete_permission(request, obj)

    @admin.action(
        permissions=["delete"],
        description="Видалити обрані групи",
    )
    def delete_selected(
        self,
        request: HttpRequest,
        queryset: QuerySet[Group],
    ) -> HttpResponse | None:
        protected = queryset.filter(name__in=PROTECTED_SYSTEM_GROUPS)
        if protected.exists():
            names = ", ".join(f"«{g.name}»" for g in protected)
            self.message_user(
                request,
                f"Видалення скасовано: групи {names} є системними для ресторану Savoure "
                "і захищені від видалення для стабільності роботи системи.",
                level=messages.ERROR,
            )
            return None
        return django_delete_selected(self, request, queryset)


# Safely replace default GroupAdmin with Savoure CustomGroupAdmin
if admin.site.is_registered(Group):
    admin.site.unregister(Group)

admin.site.register(Group, CustomGroupAdmin)
