from pingo.conf import settings as pingo_settings
from django.contrib.auth import get_user_model
from rolepermissions.roles import assign_role, remove_role
import logging

logger = logging.getLogger("error_logger")
User = get_user_model()

class ProfileTreeMixin:
    def move_profile_node_to(self, source_profile, target_profile):
        source_profile.move_to(target_profile, position="first-child")
        logger.error(f"move source_profile {source_profile} under target_profile {target_profile}")
        source_client = source_profile.client
        target_client = target_profile.client

        if target_profile.user.username == pingo_settings.SUPERUSER:
            target_client = source_profile.client
            remove_role(source_profile.user, "member")
            assign_role(source_profile.user, "client")
            if source_client.client_superadmin:
                assign_role(source_client.client_superadmin, "client_superadmin")
        else:
            remove_role(source_profile.user, "client")
            assign_role(source_profile.user, "member")
            if source_client.client_superadmin:
                remove_role(source_client.client_superadmin, "client_superadmin")

        descendants = source_profile.get_descendants(include_self=True)
        for descendant in descendants:
            descendant.client = target_client
            descendant.save()
