from rest_flex_fields import FlexFieldsModelSerializer
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from rolepermissions.roles import get_user_roles
from authentication.models import User, Client, Profile, LoggedInUser
from store.models import PointBank
from django.db.models import Sum
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from authentication.documents import UserDocument
import logging

logger = logging.getLogger("error_logger")

__all__ = [
    "TokenObtainLifetimeSerializer",
    "TokenRefreshLifetimeSerializer",
    "PingoUserCreateSerializer",
    "UserDocumentSerializer",
    "UserSerializer",
    "PingoUserSerializer",
    "LogginUserSerializer",
    "ClientSerializer",
    "ProfileSerializer",
]

class TokenObtainLifetimeSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['lifetime'] = int(refresh.access_token.lifetime.total_seconds())
        data["roles"] = [role.role_name for role in get_user_roles(self.user)]
        return data


class TokenRefreshLifetimeSerializer(TokenRefreshSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = RefreshToken(attrs['refresh'])
        data['lifetime'] = int(refresh.access_token.lifetime.total_seconds())
        data["roles"] = [role.role_name for role in get_user_roles(self.user)]
        return data


class PingoUserCreateSerializer(UserCreateSerializer):
    parent_introcode = serializers.CharField(required=False, write_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "email", "password", "parent_introcode",)
        read_only_fields = ("id",)

    def to_representation(self, instance):
        logger.error("PingoUserCreateSerializer")
        result = super().to_representation(instance)
        return result


class UserDocumentSerializer(DocumentSerializer):
    class Meta:
        document = UserDocument
        fields = (
            'id',
            'email',
            'username',
            'avatar_thumb_url'
        )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email','avatar_thumb_url',)


class PingoUserSerializer(FlexFieldsModelSerializer):
    roles = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'pk', 'email', "is_verified", "is_active", 'username', 'roles', 'introcode', 'avatar_url',
            'avatar_thumb_url', "last_login",
        )
        read_only_fields = ('pk',)

    def get_roles(self, instance):
        logger.error(instance)
        return [role.role_name for role in get_user_roles(instance)]


class LogginUserSerializer(serializers.ModelSerializer):
        user = UserSerializer(many=False)
        class Meta:
            model = LoggedInUser
            fields = "__all__"


class ClientSerializer(FlexFieldsModelSerializer):
    margin_policy = serializers.JSONField(required=False)

    class Meta:
        model = Client
        fields = ["id", 'name', 'description', "admin", "followers", "client_superadmin", "margin_policy"]
        read_only_fields = ("followers",)
        expandable_fields = {
            "admin": (PingoUserSerializer, {"many": False, "required": False}),
            "client_superadmin": (PingoUserSerializer, {"many": False, "required": False})
        }


class ProfileSerializer(FlexFieldsModelSerializer):
    margin_policy = serializers.ReadOnlyField(source="client.margin_policy")
    introcode = serializers.ReadOnlyField(source="user.introcode")
    roles = serializers.ReadOnlyField(source="user.roles")
    pointbank_balance = serializers.SerializerMethodField(source="get_pointbank_balance")
    username = serializers.ReadOnlyField(source="user.username")
    last_login = serializers.ReadOnlyField(source="user.last_login")
    is_active = serializers.ReadOnlyField(source="user.is_active")

    class Meta:
        model = Profile
        fields = ("id", 'user', "username", 'parent', "client", 'children', 'banktranser_name', 'extra_info',
                  "can_transfer_point", "margin_policy", "introcode", "get_descendants_count", "pointbank_balance",
                  "roles", "user_id","is_active","last_login")
        expandable_fields = {
            "user": PingoUserSerializer,
            "parent": PingoUserSerializer,
            "client": ClientSerializer,
        }
        read_only_fields = ('pk', 'user', 'parent', "client", "margin_policy",)

    def get_pointbank_balance(self, instance):
        mp = PointBank.objects.filter(user=instance.user).aggregate(total=Sum("point"))
        return mp["total"] if mp is not None else 0
# ProfileSerializer._declared_fields['children'] = ProfileSerializer(many=True, source='get_children', read_only=True)
