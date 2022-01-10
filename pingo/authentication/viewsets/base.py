from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenViewBase
from rolepermissions.checkers import has_role, has_permission
from rolepermissions.roles import clear_roles, assign_role, remove_role, get_user_roles
from authentication.serializers import TokenObtainLifetimeSerializer, TokenRefreshLifetimeSerializer, ClientSerializer, \
    ProfileSerializer, PingoUserSerializer, UserSerializer
from django.contrib.auth import get_user_model
from validate_email import validate_email as VALIDATE_EMAIL
from pingo.conf import settings as pingo_settings
from pingo.permissions import (IsSuperAdmin, IsStaff, IsObjectOwner, IsSupplier, StaffActionPermission)
from core.functions import PrintExceptionError
from core.mixins import PingoImageMixin
from core.elasticsearch import PaginatedElasticSearchAPIView
from authentication.permissions import ProfilePermission, UserPermission
from authentication.exceptions import OneClientExecption, SystemAssetExecption, NoAccessExecption
from authentication.models import Client, Profile, LoggedInUser
from authentication.documents import UserDocument
from authentication.mixins import ProfileTreeMixin
from django.db.models import Q
from elasticsearch_dsl import Q as Q_elasticsearch
import logging

logger = logging.getLogger("error_logger")
User = get_user_model()

__all__ = [
    "TokenObtainPairView",
    "TokenRefreshView",
    "PingoUserViewSet",
    "ProfileViewSet",
    "ClientViewSet",
    "SearchUsers",
]


class TokenObtainPairView(TokenViewBase):
    serializer_class = TokenObtainLifetimeSerializer

    def post(self, request, *args, **kwargs):
        print(request.data)
        entry_role = request.data.get("entry_role", None)
        email = request.data.get("email", None)
        user = None
        if "entry_role" in request.data and entry_role and email:
            print(f"check user role for: {request.data.get('entry_role', None)}")
            user = User.objects.filter(email=email).first()
            if not has_role(user, entry_role):
                return Response({
                    "error_code": "unmatched_role"
                }, status=status.HTTP_401_UNAUTHORIZED)
        response = super(TokenObtainPairView, self).post(request, *args, **kwargs)

        return response


class TokenRefreshView(TokenViewBase):
    serializer_class = TokenRefreshLifetimeSerializer


class PingoUserViewSet(PingoImageMixin, UserViewSet):
    permission_classes = (UserPermission,)

    def retrieve(self, request, *args, **kwargs):
        response = super(PingoUserViewSet, self).retrieve(request, *args, **kwargs)
        profile_serializer = ProfileSerializer(request.user.profile, many=False)
        response.data["profile"] = profile_serializer.data
        return Response({
            "user": response.data
        }, status=status.HTTP_200_OK)

    @action(methods=["post"], detail=True)
    def destroy_user(self, request, *args, **kwargs):
        pk = int(kwargs["id"])

        destroy_user = User.objects.filter(pk=pk).first()
        if destroy_user and destroy_user.username in pingo_settings.SYSTEM_USER_NAMES:
            raise SystemAssetExecption

        if not has_role(destroy_user, "member"):
            return Response({
                "response_code": "L01",
                "message": "not a member"
            }, status=status.HTTP_200_OK)

        self.remove_instance_old_images(destroy_user)
        logger.error("remove user avatar")
        new_parent_profile = destroy_user.profile.parent

        children_profiles = destroy_user.profile.get_children()
        for child_profile in children_profiles:
            child_profile.parent = new_parent_profile
            child_profile.save()

        request.data["email"] = destroy_user.email
        request.data["username"] = destroy_user.username

        return super(PingoUserViewSet, self).destroy(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        parent_introcode = request.data.get("parent_introcode", None)
        user_avatar = request.data.get("image", None)
        WAVUS_CLIENT = User.objects.filter(username=pingo_settings.WAVUS_CLIENT_NAME).first()

        if parent_introcode:
            parent = User.objects.filter(introcode=parent_introcode).first()
            if parent is None:
                request.data["parent_introcode"] = WAVUS_CLIENT.introcode
                logger.error("invalid parent introcode")
            else:
                logger.error("valid parent introcode, registered as child")
        else:
            request.data["parent_introcode"] = WAVUS_CLIENT.introcode
            logger.error("register as stand alone user")

        if user_avatar:
            request.data["image"] = self.suqre_crop_image(user_avatar, "avatar")

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # TODO
        # get extra information and do somthing required!

        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def avatar(self, request, *args, **kwargs):
        try:
            image = request.data.get("file", None)
            pk = request.data.get("id", None)
            logger.error(request.data)
            if pk and image:
                update_user = User.objects.get(pk=pk)
                self.replace_instance_old_images(update_user, image)
            return Response({
                "avatar_url": update_user.avatar_url,
                "avatar_thumb_url": update_user.avatar_thumb_url
            }, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({"message": PrintExceptionError(err)}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'])
    def sync_user_role(self, request, *args, **kwargs):
        try:
            logger.error(request.data)
            roles = request.data.get("roles", None)
            user = User.objects.filter(pk=kwargs["id"]).first()

            if user:
                clear_roles(user)
                for role in roles:
                    assign_role(user, role)

                serializer = self.get_serializer(user, many=False)
                return Response({
                    "user": serializer.data
                }, status=status.HTTP_200_OK)

            return Response({
                "message": "User does not exist!"
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as err:
            return Response({
                "message": PrintExceptionError(err)
            }, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['post'])
    def validate_username(self, request, *args, **kwargs):
        data = request.data
        username = data['username']
        if not str(username).isalnum():
            return Response({
                "response_code": "L01",
                "message": "username should only contain alphanumeric characters"
            }, status=status.HTTP_200_OK)

        if User.objects.filter(username=username).exists():
            return Response({
                "response_code": "L02",
                "message": "Registered username"
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "response_code": "L03",
                "message": "Not registered username"
            }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def validate_email(self, request, *args, **kwargs):
        data = request.data
        email = data['email']
        if not VALIDATE_EMAIL(email):
            return Response({
                "error_code": "L01",
                "message": "Email is invalid format"
            }, status=status.HTTP_400_BAD_REQUEST)

        if not User.objects.filter(email=email).exists():
            return Response({
                "message": "Not registered email"
            }, status=status.HTTP_200_OK)
        elif User.objects.filter(email=email, is_active=False).exists():
            return Response({
                "error_code": "L03",
                "message": "Registered but not active email"
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                "error_code": "L04",
                "message": "Registered and verified email"
            }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post", "get"])
    def validate_token(self, request, *args, **kwargs):
        return Response({}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def validate_userid(self, request, id=None):
        user = User.objects.filter(pk=id).first()
        logger.error(user)
        logger.error(has_role(user, ["member", "client"]))
        if user and has_role(user, ["member", "client"]):
            return Response({
                "error_code": "L01",
                "user": {
                    "id": id,
                    "username": user.username
                },
                "valid_role": has_role(user, ["member", "client"]),
                "message": "valid user id"
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "error_code": "L02",
                "message": "invalid user id"
            }, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"])
    def validate_transfer_user_ids(self, request, id=None):
        from_id = request.data.get("from_id", None)
        to_id = request.data.get("to_id", None)
        from_user = User.objects.get(pk=from_id)
        to_user = User.objects.get(pk=to_id)

        if not has_role(to_user, ["member", "client", "supplier", "staff"]):
            return Response({
                "error_code": "L01",
                "message": "移動さきは member, client, supplierとstaffのみ。",
                "to_user": [role.role_name for role in get_user_roles(from_user)],
            }, status=status.HTTP_400_BAD_REQUEST)

        if not has_role(from_user, ["member", "client"]):
            return Response({
                "error_code": "L02",
                "message": "選択会員は member あるいは clientではない",
                "from_user": [role.role_name for role in get_user_roles(from_user)],
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "from_user": {
                "id": from_user.id,
                "username": from_user.username
            },
            "to_user": {
                "id": to_user.id,
                "username": to_user.username
            }
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def validate_verification_status(self, request, *args, **kwargs):
        data = request.data
        email = data['email']
        if not User.objects.filter(email=email).exists():
            return Response({
                "errors": "LE01"  # 'Not a registered email.'
            }, status=status.HTTP_200_OK)

        if User.objects.filter(email=email, is_verified=False).exists():
            return Response({
                "errors": "LE02"  # 'Registered but not verified'}
            }, status=status.HTTP_200_OK)

        if User.objects.filter(email=email, is_active=False).exists():
            return Response({
                "errors": "LE03"  # 'Verified but not actived.'
            }, status=status.HTTP_200_OK)

        return Response({
            "errors": "LE00"
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def verify_introcode(self, request, *args, **kwargs):
        try:
            introcode = request.data.get('introcode', None)
            logger.error("introcode {}".format(introcode))
            user = User.objects.filter(introcode=introcode).first()
            if user:
                return Response({
                    "result": True,
                    "data": {
                        "username": user.username,
                        "email": user.email,
                        "id": user.id
                    }
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "error_code": "VerificationCode_01",
                    "message": "introcode user does not exist."
                }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                "result": False,
                "error": "VerificationCode_02",
                "message": "invalid introcode"
            }, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def filter_users(self, request, *args, **kwargs):

        key_str = request.query_params.get("key_str")
        logger.error(key_str)
        users = User.objects.filter(Q(username__icontains=key_str) | Q(email__icontains=key_str))
        serializer = PingoUserSerializer(users, many=True)
        return Response({
            "users": serializer.data
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def activation_status(self, request, *args, **kwargs):
        email = request.query_params.get('email', None)
        if email is None:
            return Response({
                "error_code": "LE00",
                "message": "email is required"
            }, status=status.HTTP_200_OK)

        if not User.objects.filter(email=email).exists():
            return Response({
                "error_code": "LE01",
                "message": "Not a registered email."
            }, status=status.HTTP_200_OK)

        if User.objects.filter(email=email, is_active=False).exists():
            return Response({
                "error_code": "LE03",
                "message": "email is not actived"
            }, status=status.HTTP_200_OK)

        return Response({
            "error_code": "LE04"
        }, status=status.HTTP_200_OK)


class ProfileViewSet(ProfileTreeMixin, ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = (ProfilePermission,)

    @action(methods=["post"], detail=True)
    def retrieve_children(self, request, pk=None, *args, **kwargs):
        try:
            user = User.objects.get(pk=pk)
            serializer = self.get_serializer(instance=user.profile.get_children(), many=True)

            return Response({
                "children": serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({
                "response_code": "L01",
                "message": "valid user id",
                'extra_message":"': PrintExceptionError(err)
            }, status=status.HTTP_200_OK)

    @action(methods=["post"], detail=True)
    def retrieve_descendants(self, request, pk=None, *args, **kwargs):
        try:
            # users = User.objects.filter(profile__client_id=pk)
            # serializer = PingoUserSerializer(instance=users, many=True)
            profiles = Profile.objects.filter(client_id=pk)
            serializer = self.get_serializer(profiles, many=True)
            return Response({
                "children": serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({
                'extra_message":"': PrintExceptionError(err)
            }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["post"])
    def move_to_client_member(self, request, pk=None):
        try:
            parent_id = request.data.get("parent_id", None)
            user = User.objects.get(pk=pk)
            parent = User.objects.get(pk=parent_id)

            if not has_role(user, ["member", "client"]):
                return Response({
                    "error_code": "L01",
                    "message": "from user Must be member or client",
                    "from user": [role.role_name for role in get_user_roles(user)],
                }, status=status.HTTP_400_BAD_REQUEST)

            if not has_role(parent, ["member", "client", "supplier", "staff"]):
                return Response({
                    "error_code": "L02",
                    "message": "to user Must be member ,client,supplier or staff",
                    "to user": [role.role_name for role in get_user_roles(parent)],
                }, status=status.HTTP_400_BAD_REQUEST)

            # if user.profile and parent.profile:
            user_profile = user.profile
            parent_profile = parent.profile
            user_profile.move_to(parent_profile, position='first-child')

            isClient = has_role(user, "client")
            client_superadmin = user_profile.client.client_superadmin if isClient else None

            descendants = user_profile.get_descendants(include_self=True)

            for child_profile in descendants:
                child_profile.client = parent_profile.client
                child_profile.save()

                clear_roles(child_profile.user)
                assign_role(child_profile.user, "member")

            if client_superadmin:
                remove_role(user_profile.client.client_superadmin, "client_superadmin")
            if isClient:
                Client.objects.filter(admin=user).delete()

            return Response({
                "message": "move user and descendants under target user",
            }, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({
                "error_code": "L04",
                "extra_message": PrintExceptionError(err)
            }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["post"])
    def move_to_management_member(self, request, pk=None):
        try:
            parent_id = request.data.get("parent_id", None)
            user = User.objects.get(pk=pk)
            parent = User.objects.get(pk=parent_id)

            if not has_role(user, "member"):
                return Response({
                    "response_code": "L01",
                    "message": "User must be member",
                }, status=status.HTTP_200_OK)

            if not has_role(parent, "staff") and not has_role(parent, "supplier"):
                return Response({
                    "response_code": "L02",
                    "message": "target must be staff or supplier group",
                    "to user": [role.role_name for role in get_user_roles(parent)],
                }, status=status.HTTP_200_OK)

            parent_role = "staff" if has_role(parent, "staff") else "supplier"
            # if user.profile and parent.profile:
            user_profile = user.profile
            parent_profile = parent.profile
            user_profile.move_to(parent_profile, position='first-child')

            descendants = user_profile.get_descendants(include_self=True)

            for child_profile in descendants:
                child_profile.client = None
                clear_roles(child_profile.user)
                assign_role(child_profile.user, parent_role)
                child_profile.save()

            return Response({
                "response_code": "L03",
                "message": "move user to management group withour client information",
            }, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({
                "response_code": "L04",
                "message": "Matching error?",
                "extra_message": PrintExceptionError(err)
            }, status=status.HTTP_200_OK)


class ClientViewSet(ProfileTreeMixin, ModelViewSet):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()
    permission_classes = (StaffActionPermission,)

    def create(self, request, *args, **kwargs):

        try:
            client_admin_id = request.data.get("admin", None)
            request.data.pop("admin")
            client_admin = User.objects.get(pk=client_admin_id)

            client_superadmin_id = request.data.get("client_superadmin", None)
            client_superadmin = None
            if client_superadmin_id:
                request.data.pop("client_superadmin")
                client_superadmin = User.objects.get(pk=client_superadmin_id)

            client = Client.objects.filter(admin=client_admin).first()
            if client:
                raise OneClientExecption

            logger.error(request.data)
            serializer = self.get_serializer(data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            new_client = serializer.save(admin=client_admin)

            if client_superadmin:
                logger.error(f"add client_superadmin: {new_client}")
                new_client.client_superadmin = client_superadmin
                new_client.save()

            logger.error(f"new_client: {new_client}")
            client_admin.profile.client = new_client
            client_admin.profile.save()

            SUPERUSER = User.objects.get(username=pingo_settings.SUPERUSER)
            self.move_profile_node_to(client_admin.profile, SUPERUSER.profile)

            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        except Exception as err:
            return Response({
                "message": PrintExceptionError(err)
            }, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None, *args, **kwargs):

        client = Client.objects.get(pk=pk)
        WAVUS_CLIENT_USER = User.objects.get(username=pingo_settings.WAVUS_CLIENT_NAME)

        # WAVUS_CLIENT can not be removed
        if client.name in pingo_settings.SYSTEM_CLIENT_NAMES:
            raise SystemAssetExecption

        self.move_profile_node_to(client.admin.profile, WAVUS_CLIENT_USER.profile)

        return super(ClientViewSet, self).destroy(request, pk, *args, **kwargs)


class SearchUsers(PaginatedElasticSearchAPIView):
    serializer_class = UserSerializer
    document_class = UserDocument

    def generate_q_expression(self, query):
        return Q_elasticsearch('bool',
                               should=[
                                   Q_elasticsearch('wildcard', username=query),
                                   Q_elasticsearch('wildcard', email=query),
                               ], minimum_should_match=1)
