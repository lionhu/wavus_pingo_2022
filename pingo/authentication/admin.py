from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Client, Profile
import os
from django.utils.html import format_html
from mptt.admin import MPTTModelAdmin
from rolepermissions.roles import get_user_roles
import json


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'is_active','is_verified', 'roles', "thumbimage",)
    list_editable = ('is_active','is_verified')
    list_filter = ('is_active',)
    readonly_fields = ('thumbimage',)

    def thumbimage(self, instance):
        if instance.image:
            tmpl = '<img style="max-width:60px;" src="{}" onClick="window.open(\'{}\', \'{}\');" />'
            basename = os.path.basename(instance.image.url)
            return format_html(
                tmpl, instance.thumbimage.url, instance.image.url, basename)

    def roles(self, instance):
        user_roles = get_user_roles(instance)
        if user_roles:
            tmpl = "<ul>"
            for role in user_roles:
                tmpl += "<li>{}</li>".format(role.role_name)
            tmpl += "</ul>"
            return format_html(tmpl)


class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'admin', 'client_superadmin',)


class ProfileAdmin(MPTTModelAdmin):
    list_display = ('user','roles', 'parent', 'client', 'can_transfer_point', )
    # readonly_fields = ('parent', 'client',)
    mptt_level_indent = 20

    def roles(self, instance):
        user_roles = get_user_roles(instance.user)
        if user_roles:
            tmpl = "<ul>"
            for role in user_roles:
                tmpl += "<li>{}</li>".format(role.role_name)
            tmpl += "</ul>"
            return format_html(tmpl)

admin.site.register(Client, ClientAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(User, UserAdmin)
