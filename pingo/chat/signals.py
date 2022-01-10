from django.dispatch import Signal
from django.dispatch import receiver
import logging
# from .models import Message
# from authentication.models import LoggedInUser
logger = logging.getLogger("error_logger")

signalNewMessage = Signal(providing_args=["message"])


@receiver(signalNewMessage)
def record_new_message(sender, **kwargs):
    logger.error("record_newMessage")
    logger.error(kwargs)
    # LoggedInUser.objects.create(
    #     user_id=1,
    #     web=True
    # )
