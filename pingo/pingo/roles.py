from rolepermissions.roles import AbstractUserRole


class Superadmin(AbstractUserRole):
    role_name = "superadmin"
    available_permissions = {
        "add_client": True,
        "update_client": True,
        "destroy_client": True,

        "delete_category": True,
        "update_category": True,
        "create_category": True,

    }


class Staff(AbstractUserRole):
    role_name = "staff"
    available_permissions = {
        'view_followers': True,
        'view_all_vendors': False,
        'place_order': False,
        'enter_backend': True,

        "delete_category": False,
        "update_category": True,
        "create_category": True,

    }


class Client(AbstractUserRole):
    role_name = "client"
    available_permissions = {
        'view_followers': True,
        'view_all_vendors': False,
    }


class ClientSuperAdmin(AbstractUserRole):
    role_name = "client_superadmin"
    available_permissions = {
        'view_followers': True,
        'view_all_vendors': False,
        'place_order': False,
        'enter_backend': True,

        "delete_category": False,
        "update_category": True,
        "create_category": True,

    }


class Member(AbstractUserRole):
    role_name = "member"
    available_permissions = {
        'place_order': True,
        'enter_backend': False
    }


class Supplier(AbstractUserRole):
    role_name = "supplier"
    available_permissions = {
        'place_order': False,
        'enter_backend': False
    }
