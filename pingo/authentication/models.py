from django.db import models
from django.conf import settings
import os
import uuid
import json
from jsonfield import JSONField
from mptt.models import MPTTModel, TreeForeignKey
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from rolepermissions.roles import get_user_roles
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from pingo.conf import settings as pingo_settings
from rolepermissions.roles import assign_role
import logging

logger = logging.getLogger("error_logger")


class CustomUserManager(BaseUserManager):

    def create_user_base(self, username, email, password=None, **extra_fields):
        logger.error("CustomUserManager create_user_base: extra_fields")
        if not email:
            raise ValueError("User must have an email")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_profile(self, user, parent_profile, client):
        profile = Profile.objects.create(user=user, parent=parent_profile, client=client)
        logger.error(f"user {user} profile has been setup!")
        return profile

    def create_superuser(self, username, email, password=None, **extra_fields):
        user = self.create_user_base(pingo_settings.SUPERUSER, email, password=password, **extra_fields)
        user.is_active = True
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.introcode = f"{str(uuid.uuid4())}_{user.id}"
        user.save()

        assign_role(user, "superadmin")
        self.create_profile(user, None, None)

        return user

    def create_staff(self, username, email, password=None, **extra_fields):
        user = self.create_user_base(username, email, password=password, **extra_fields)
        user.is_active = True
        user.is_staff = True
        user.introcode = f"{str(uuid.uuid4())}_{user.id}"
        user.save()

        assign_role(user, "staff")

        wavus_group_user = User.objects.filter(username=pingo_settings.WAVUS_GROUP_NAME).first()

        if wavus_group_user and wavus_group_user.profile:
            self.create_profile(user, wavus_group_user.profile, None)
            user.profile.client = wavus_group_user.profile.client
            user.profile.save()

        return user

    def create_supplier(self, username, email, password=None, **extra_fields):
        user = self.create_user_base(username, email, password=password, **extra_fields)
        user.is_active = True
        user.is_staff = True
        user.introcode = f"{str(uuid.uuid4())}_{user.id}"
        user.save()

        assign_role(user, "supplier")

        supplier_group_user = User.objects.filter(username=pingo_settings.SUPPLIER_GROUP_NAME).first()

        if supplier_group_user and supplier_group_user.profile:
            self.create_profile(user, supplier_group_user.profile, None)

        return user

    def create_management_group(self, username, email, password=None, **extra_fields):
        user = self.create_user_base(username, email, password=password, **extra_fields)
        user.is_active = True
        user.introcode = f"{str(uuid.uuid4())}_{user.id}"
        user.save()

        SUPERUSER = User.objects.filter(username=pingo_settings.SUPERUSER).first()
        self.create_profile(user, SUPERUSER.profile, None)

        return user

    def create_client_user(self, username, email, password=None, **extra_fields):
        user = self.create_user_base(username, email, password=password, **extra_fields)
        user.introcode = f"{str(uuid.uuid4())}_{user.id}"
        user.save()

        assign_role(user, "client")
        client = Client.objects.create(name=username, admin=user,
                                       margin_policy=pingo_settings.SHOP_SETTINGS.DEFAULT_MARGIN_POLICY)

        SUPERUSER = User.objects.filter(username=pingo_settings.SUPERUSER).first()
        self.create_profile(user, SUPERUSER.profile, client)

        return user

    def create_user(self, username, email, password=None, **extra_fields):
        user = self.create_user_base(username, email, password=password, **extra_fields)
        user.introcode = f"{str(uuid.uuid4())}_{user.id}"
        user.save()
        assign_role(user, "member")

        parent_introcode = extra_fields.get("parent_introcode", None)

        if parent_introcode:
            parent = User.objects.filter(introcode=parent_introcode).first()
            if parent:
                self.create_profile(user, parent.profile, parent.profile.client)
                return user

        parent = User.objects.filter(username=pingo_settings.WAVUS_CLIENT_NAME).first()
        self.create_profile(user, parent.profile, parent.profile.client)
        return user


def image_path(instance, filename):
    extension = filename.split(".")[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex[:10], extension)
    file_path = os.path.join("avatar", "images", filename)
    return file_path


class User(AbstractBaseUser, PermissionsMixin):
    class Meta:
        ordering = ['id']

    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=True)
    introcode = models.CharField(max_length=255, blank=True, null=True, default="")
    parent_introcode = models.CharField(max_length=255, blank=True, null=True, default=None)
    login_count = models.IntegerField(default=0)

    image = models.ImageField(null=True, blank=True, default="default.jpg", upload_to=image_path)
    thumbimage = ImageSpecField(
        source='image',
        processors=[ResizeToFill(256, 256)],
        format='JPEG',
        options={'quality': 95}
    )
    last_location = JSONField(blank=True, null=True, default=dict)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def get_full_name(self):
        return f"{self.first_name} - {self.last_name}"

    def get_short_name(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def __str__(self):
        return self.email

    @property
    def roles_indexing(self):
        roles = [role.role_name for role in get_user_roles(self)]
        return json.dumps(roles)

    @property
    def last_location_indexing(self):
        return json.dumps(self.last_location)

    @property
    def client_name_indexing(self):
        if self.profile.client is not None:
            return self.profile.client.name
        return "NA"

    @property
    def can_transfer_indexing(self):
        return self.profile.can_transfer_point

    @property
    def avatar_url(self):
        image_url = self.image.url if self.image is not None else '/mediafiles/avatar.png'
        return f"{pingo_settings.WEBSITE}{image_url}"

    @property
    def avatar_thumb_url(self):
        image_url = self.thumbimage.url if self.thumbimage is not None else '/mediafiles/avatar.png'
        return f"{pingo_settings.WEBSITE}{image_url}"


class LoggedInUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='logged_in_user')
    web = models.BooleanField(default=False)
    ws_channel = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Profile(MPTTModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    client = models.ForeignKey("Client", blank=True, null=True, on_delete=models.SET_NULL)
    banktranser_name = models.CharField(max_length=50, blank=True, null=True)
    extra_info = JSONField(blank=True, null=True, default=dict)
    can_transfer_point = models.BooleanField(blank=True, null=True, default=False)

    # class MPTTMeta:
    #     order_insertion_by = ['introcode']

    def __str__(self):
        return self.user.username

    @property
    def get_descendants_count(self):
        return self.get_descendants(include_self=False).count()

    @property
    def parent_indexing(self):
        return self.parent.id if self.parent else 0


class Client(models.Model):
    name = models.CharField(default="", blank=True, null=True, max_length=50)
    admin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                              related_name="admin_client")
    client_superadmin = models.ForeignKey("User", on_delete=models.SET_NULL,
                                          blank=True, null=True, related_name="superadmin_client")
    description = models.CharField(default="", blank=True, null=True, max_length=50)
    margin_policy = JSONField(default=pingo_settings.SHOP_SETTINGS.DEFAULT_MARGIN_POLICY, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def followers(self):
        return Profile.objects.filter(client=self).count()

    @property
    def admin_name(self):
        return self.admin.username

    @property
    def superadmin_name(self):
        return self.client_superadmin.username
