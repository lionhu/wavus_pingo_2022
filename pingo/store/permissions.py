from rest_framework.permissions import (
    AllowAny, BasePermission, IsAdminUser, IsAuthenticated
)
from rest_action_permissions.permissions import ActionPermission
from pingo.permissions import (IsClient, IsSuperAdmin, IsStaff, IsObjectOwner, IsSupplier, StaffActionPermission)
import logging

logger = logging.getLogger("error_logger")


class SupplierPermission(ActionPermission):
    # The admin user has all permissions.
    enough_perms = IsStaff

    read_perms = IsSupplier
    create_perms = IsSupplier
    retrieve_perms = IsSupplier
    list_perms = IsStaff
    update_perms = IsSupplier | IsStaff
    destroy_perms = IsStaff
    retrieve_by_email_perms = IsSupplier


class PointBankPermission(ActionPermission):
    # The admin user has all permissions.
    enough_perms = IsStaff

    read_perms = IsAuthenticated
    create_perms = IsObjectOwner
    retrieve_perms = IsObjectOwner
    list_perms = IsAuthenticated
    update_perms = IsObjectOwner | IsStaff
    destroy_perms = IsObjectOwner
    me_perms = IsAuthenticated
    summary_perms = IsAuthenticated

    admin_list_perms = IsStaff | IsClient


class MarginPermission(ActionPermission):
    # The admin user has all permissions.
    enough_perms = IsStaff

    read_perms = IsAuthenticated
    create_perms = IsStaff
    retrieve_perms = IsStaff
    list_perms = IsStaff
    update_perms = IsStaff
    update_batch_perms = IsStaff
    destroy_perms = IsStaff
    me_perms = IsAuthenticated


class AddressBookPermission(ActionPermission):
    # The admin user has all permissions.
    enough_perms = IsStaff

    create_perms = IsObjectOwner
    retrieve_perms = IsObjectOwner
    list_perms = IsAuthenticated
    update_perms = IsObjectOwner | IsStaff
    destroy_perms = IsObjectOwner


class CommentPermission(ActionPermission):
    # The admin user has all permissions.
    enough_perms = IsStaff

    create_perms = IsObjectOwner
    list_perms = AllowAny
    create_pingo_perms = IsObjectOwner
    list_pingo_perms = AllowAny
    retrieve_perms = AllowAny
    update_perms = IsObjectOwner | IsStaff
    update_batch_perms = IsStaff
    destroy_perms = IsObjectOwner
    approve_perms = AllowAny
    read_perms = AllowAny


class PingoProductPermission(ActionPermission):
    # The admin user has all permissions.
    enough_perms = IsSuperAdmin

    create_perms = IsStaff
    retrieve_perms = AllowAny
    list_perms = AllowAny
    list_recruiting_perms = AllowAny
    update_perms = IsStaff
    destroy_perms = IsStaff
    get_introduce_qr_perms = IsAuthenticated

    write_perms = IsStaff


class ProductPermission(ActionPermission):
    # The admin user has all permissions.
    enough_perms = IsSuperAdmin

    create_perms = IsStaff | IsSupplier
    retrieve_perms = AllowAny
    list_perms = AllowAny
    list_recruiting_perms = AllowAny
    update_perms = IsStaff | IsSupplier
    destroy_perms = IsStaff
    update_post_image_perms = IsStaff | IsSupplier
    get_introduce_qr_perms = IsAuthenticated


class ItemSliderImagePermission(ActionPermission):
    # The admin user has all permissions.
    enough_perms = IsSuperAdmin

    create_perms = IsStaff | IsSupplier
    retrieve_perms = AllowAny
    list_perms = AllowAny
    list_recruiting_perms = AllowAny
    update_perms = IsStaff | IsSupplier
    destroy_perms = IsStaff | IsSupplier
    update_post_image_perms = IsStaff | IsSupplier


class VariationImagePermission(ActionPermission):
    # The admin user has all permissions.
    enough_perms = IsSuperAdmin

    create_perms = IsStaff | IsSupplier
    retrieve_perms = AllowAny
    list_perms = AllowAny
    list_recruiting_perms = AllowAny
    update_perms = IsStaff | IsSupplier
    destroy_perms = IsStaff | IsSupplier
    update_image_perms = IsStaff | IsSupplier
