from django.contrib.auth.management.commands import createsuperuser
from django.core.management import CommandError
from django.conf import settings
from pingo.conf import settings as pingo_settings
from rolepermissions.roles import assign_role
from django.contrib.auth import get_user_model
from authentication.models import Profile, Client
import uuid
import logging

logger = logging.getLogger("error_logger")
User = get_user_model()


class Command(createsuperuser.Command):
    help = 'Create a superuser with a password non-interactively'
    database = settings.DATABASES["default"]

    def handle(self, *args, **options):
        superuser = User.objects.create_superuser(pingo_settings.SUPERUSER, "superadmin@wavus.jp", "Lionhu2008")

        print("superuser created")
        supplier_group_user = User.objects.create_management_group(pingo_settings.SUPPLIER_GROUP_NAME,
                                                                   "supplier_group@wavus.jp", "Lionhu2008")
        assign_role(supplier_group_user, "supplier")
        print("supplier_group_user created")

        supplier_user = User.objects.create_supplier("supplier", "supplier@wavus.jp", "Lionhu2008")
        assign_role(supplier_user, "supplier")
        print("supplier_user created")

        wavus_group_user = User.objects.create_management_group(pingo_settings.WAVUS_GROUP_NAME,
                                                                "wavus_group@wavus.jp", "Lionhu2008")
        assign_role(wavus_group_user, "staff")
        print("wavus_group_user created")

        staff_user = User.objects.create_staff("staff", "staff@wavus.jp", "Lionhu2008")
        assign_role(staff_user, "staff")
        print("staff_user created")

        wavus_client_user = User.objects.create_client_user(pingo_settings.WAVUS_CLIENT_NAME, "wavus_client@wavus.jp",
                                                            "Lionhu2008")
        print("wavus_client_user created")


        print("Well Done!")
