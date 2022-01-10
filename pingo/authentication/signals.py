from djoser.signals import user_registered, user_activated
from django.contrib.auth import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, post_delete
from .models import LoggedInUser, Profile
from .emails import NotificationRegisterEmail
from django.contrib.auth import get_user_model
import logging

logger = logging.getLogger("error_logger")
User = get_user_model()


@receiver(user_activated)
def on_user_activated(user, request, **kwargs):
    context = {"user": user}
    NotificationRegisterEmail(request, context).send(["huhaiguang@me.com"])


@receiver(user_registered)
def on_user_registered(user, request, **kwargs):
    context = {"user": user}
    NotificationRegisterEmail(request, context).send(["huhaiguang@me.com"])


@receiver(user_logged_in)
def on_user_login(sender, **kwargs):
    LoggedInUser.objects.get_or_create(user=kwargs.get('user'), web=True)


@receiver(user_logged_out)
def on_user_logout(sender, **kwargs):
    LoggedInUser.objects.filter(user=kwargs.get('user'), web=True).delete()


@receiver(post_delete)
def post_delete_model(sender, instance, **kwargs):
    app_label = sender._meta.app_label
    model_name = sender._meta.model_name
    logger.error(kwargs)

    # logger.error(f"post_delete_model {app_label}: {model_name}")
    # if app_label == "authentication":
    #     if model_name == "user":
    #         if instance.id is not None:



@receiver(pre_save)
def pre_save_model(sender, instance, **kwargs):
    app_label = sender._meta.app_label
    model_name = sender._meta.model_name

    # logger.error(f"pre_save_model {app_label}: {model_name}")

    # if app_label == "authentication":
    #     if model_name == "user":
    #         if instance.id is not None:

@receiver(post_save)
def after_save_object(sender, instance, **kwargs):
    app_label = sender._meta.app_label
    model_name = sender._meta.model_name

    # logger.error(f"pre_save {app_label}: {model_name}")

    # if app_label == "authentication":
    #     if model_name == "user":
            # if instance.image is not None:
            #     instance.image = suqre_crop_image(instance.image, "'avatar.jpg'")
            #     instance.save()
