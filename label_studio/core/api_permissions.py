from rest_framework.permissions import BasePermission

from pathlib import Path
import json


def is_admin_task(request, view, obj):
    if (
        "delete" in str(vars(request)).lower()
        or "delete" in str(vars(view))
        or "delete" in str(vars(obj))
    ):
        # import ipdb; ipdb.set_trace()
        return True
    return False


def is_admin_user(request, admin_info):
    em = request.user.email
    if em not in admin_info:
        return False
    if admin_info[em].get("role", "") == "admin":
        return True
    return False


class HasObjectPermission(BasePermission):
    perm_file = Path.home() / "labelstudio_permissions.json"
    admin_info = json.loads(perm_file.read_text())

    def has_object_permission(self, request, view, obj):
        if is_admin_task(request, view, obj):
            if is_admin_user(request, HasObjectPermission.admin_info):
                return True
            return False
        return obj.has_permission(request.user)
