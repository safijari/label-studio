from rest_framework.permissions import BasePermission

from pathlib import Path
import json


non_admin_allowed = {
    "projects.view",
    "organizations.view",
    "tasks.view",
    "tasks.change",
    "annotations.view",
    "annotations.change",
    "labels.create",
    "labels.view",
    "labels.change",
    "labels.delete",
}


def is_admin_task(request, view, obj):
    rm = request._request.method  # PATCH
    pr = view.permission_required
    try:
        if not isinstance(pr, str):
            pr = view.permission_required.__getattribute__(rm)
        print(pr, rm, request._request.path)
        if pr not in non_admin_allowed:
            return True
    except Exception:
        import ipdb
        ipdb.set_trace()
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
    if perm_file.exists():
        admin_info = json.loads(perm_file.read_text())
    else:
        admin_info = {}

    def has_object_permission(self, request, view, obj):
        if is_admin_task(request, view, obj):
            if is_admin_user(request, HasObjectPermission.admin_info):
                return True
            return False
        return obj.has_permission(request.user)
