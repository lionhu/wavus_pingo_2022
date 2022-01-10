from rest_framework.permissions import (AllowAny, IsAuthenticated)
from pingo.permissions import (IsSuperAdmin, IsStaff, IsObjectOwner, IsSupplier, StaffActionPermission)

from rest_action_permissions.permissions import ActionPermission

import logging

logger = logging.getLogger("error_logger")


class ProfilePermission(ActionPermission):
    # The admin user has all permissions.
    enough_perms = IsSuperAdmin

    # Corresponding permissions for each action.
    create_perms = IsSuperAdmin
    retrieve_perms = IsObjectOwner | IsStaff
    list_perms = IsStaff
    update_perms = IsObjectOwner | IsStaff
    destroy_perms = IsSuperAdmin
    retrieve_children_perms = IsObjectOwner | IsStaff
    retrieve_descendants_perms = IsObjectOwner | IsStaff
    move_to_client_member_perms = IsStaff
    move_to_management_member_perms = IsStaff
    filter_users_perms = IsStaff

    # General read/write permissions.
    # Used if corresponding action permission hasn't been specified.
    # read_perms = IsObjectOwner
    # write_perms = IsSuperAdmin


class UserPermission(ActionPermission):
    # The admin user has all permissions.
    enough_perms = IsSuperAdmin

    # Corresponding permissions for each action.
    create_perms = AllowAny
    retrieve_perms = IsAuthenticated
    list_perms = IsStaff
    update_perms = IsAuthenticated
    destroy_perms = IsSuperAdmin
    destroy_user_perms = IsSuperAdmin
    retrieve_children_perms = IsAuthenticated
    retrieve_descendants_perms = IsAuthenticated
    me_perms = IsAuthenticated
    avatar_perms = IsAuthenticated
    sync_user_role_perms = IsStaff
    validate_username_perms = AllowAny
    validate_email_perms = AllowAny
    validate_token_perms = AllowAny
    validate_userid_perms = AllowAny
    validate_verification_status_perms = AllowAny
    activation_status_perms = AllowAny
    verify_introcode_perms = AllowAny
    filter_users_perms = AllowAny
    validate_transfer_user_ids_perms = IsStaff

    # General read/write permissions.
    # Used if corresponding action permission hasn't been specified.
    read_perms = AllowAny
    # write_perms = IsSuperAdmin
