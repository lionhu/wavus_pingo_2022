from celery import shared_task
from store.models import ViewProductHistory, Variation, InventoryHistory, Order, OrderItem, Margin, PingoItem
from core.functions import PrintExceptionError
from pingo.conf import settings as pingo_settings
from django.core.cache import cache
import logging

logger = logging.getLogger("error_logger")

__all__ = [
    "recore_viewproduct_event",
    "common_notification",
]


@shared_task(name="recore_viewproduct_event")
def recore_viewproduct_event(item_id, user_id, type):
    try:
        print(f"recore_viewproduct_event ,user_id: {user_id},product_id: {item_id},type:{type}")
        obj, created = ViewProductHistory.objects.update_or_create(
            user_id=user_id,
            item_id=item_id,
            type=type,
            defaults={
                "user_id": user_id,
                "item_id": item_id,
                "type": type,
            }
        )
        if created:
            redis_key = pingo_settings.REDIS_KEYS["VIEW_HISTORIES"].format(user_id)
            cache.delete(redis_key)

    except Exception as err:
        logger.error(PrintExceptionError(err))


@shared_task(name="common_notification")
def common_notification(to_email,content):
    try:
        context = {
            "subject": "通知",
            "type": "Common",
            "content": content,
            "button_blue_text": f"管理ログイン",
            "button_blue_url": f"https://www.pingo.jp//backend/account/login",
            "button_grey_text": "Shop ログイン",
            "button_grey_url": f"https://www.pingo.jp",
        }
        pingo_settings.EMAIL.common_notification(context=context).send([to_email])

    except Exception as err:
        logger.error(PrintExceptionError(err))


