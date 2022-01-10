from rolepermissions.checkers import has_role
from rest_framework.permissions import (BasePermission, AllowAny)
from rest_action_permissions.permissions import ActionPermission
import logging

logger = logging.getLogger("error_logger")


class IsSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        logger.error(f"request user: {request.user}")
        logger.error(f"IsSuperAdmin has_permission: {has_role(request.user, 'superadmin')}")
        return has_role(request.user, "superadmin")

    def has_object_permission(self, request, view, obj):
        logger.error(f"IsSuperAdmin has_object_permission: {has_role(request.user, 'superadmin')}")
        return has_role(request.user, "superadmin")


class IsStaff(BasePermission):
    def has_permission(self, request, view):

        logger.error(f"request user: {request.user}")
        logger.error(
            f"IsStaff has_permission: {has_role(request.user, 'staff') or has_role(request.user, 'superadmin')}")

        return has_role(request.user, "staff") or has_role(request.user, "superadmin")

    def has_object_permission(self, request, view, obj):
        logger.error(f"IsStaff has_object_permission: {has_role(request.user, 'staff') or has_role(request.user, 'superadmin')}")
        return has_role(request.user, "staff") or has_role(request.user, "superadmin")


class IsSupplier(BasePermission):
    def has_permission(self, request, view):
        print(f"IsSupplier has_permission:{has_role(request.user, 'supplier')}")
        return has_role(request.user, "supplier")

    def has_object_permission(self, request, view, obj):
        return has_role(request.user, "supplier")

class IsClient(BasePermission):
    def has_permission(self, request, view):
        print(f"IsClient has_permission:{has_role(request.user, 'client')}")
        return has_role(request.user, "client")

    def has_object_permission(self, request, view, obj):
        return has_role(request.user, "client")


class IsObjectOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class StaffActionPermission(ActionPermission):
    # The admin user has all permissions.
    enough_perms = IsSuperAdmin

    read_perms = IsStaff
    write_perms = IsStaff


class SAFEActionPermission(ActionPermission):
    enough_perms = IsSuperAdmin

    read_perms = AllowAny
    write_perms = IsStaff
