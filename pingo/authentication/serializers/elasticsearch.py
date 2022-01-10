from rest_framework.serializers import ModelSerializer
from rolepermissions.roles import get_user_roles
from authentication.models import User, Client, Profile, LoggedInUser
import logging

logger = logging.getLogger("error_logger")

__all__ = [
    "BasicUserElasticSearchSerializer",
    "BasicClientElasticSearchSerializer",
    "UserElasticSearchSerializer",
    "ProfileElasticSearchSerializer",
    "ActiveUserElasticSearchSerializer",
]


class BasicUserElasticSearchSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'avatar_thumb_url',
            'email'
        )


class BasicClientElasticSearchSerializer(ModelSerializer):
    class Meta:
        model = Client
        fields = (
            'id',
            'name',
            'admin_name',
            'superadmin_name'
        )


class UserElasticSearchSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'introcode',
            'parent_introcode',
            'avatar_thumb_url',
            'last_login',
            'login_count',
            'is_active',
        )


class ProfileElasticSearchSerializer(ModelSerializer):
    user = UserElasticSearchSerializer(many=False)

    class Meta:
        model = Profile
        fields = (
            'id',
            'can_transfer_point',
            'parent_indexing',
            'get_descendants_count',
            'user',
        )

    def to_representation(self, instance):
        result = super(ProfileElasticSearchSerializer, self).to_representation(instance)
        user = User.objects.get(pk=instance.user["id"])
        result["user"]["roles"] = [role.role_name for role in get_user_roles(user)]
        result["user"]["last_location"] = user.last_location
        return result


class ActiveUserElasticSearchSerializer(ModelSerializer):
    user = BasicUserElasticSearchSerializer(many=False)

    class Meta:
        model = LoggedInUser
        fields = (
            'id',
            'web',
            'ws_channel',
            'created_at',
            "user"
        )
