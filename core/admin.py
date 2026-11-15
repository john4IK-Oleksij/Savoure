from typing import Final

from django.contrib import admin, messages
from django.contrib.admin.actions import delete_selected as django_delete_selected
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.models import Group
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse

PROTECTED_SYSTEM_GROUPS: Final[frozenset[str]] = frozenset({"Chef", "Manager"})


class CustomGroupAdmin(GroupAdmin):
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
