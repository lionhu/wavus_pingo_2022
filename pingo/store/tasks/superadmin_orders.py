from celery import shared_task
from core.functions import PrintExceptionError
from pingo.conf import settings as pingo_settings
from store.models import OrderItem, Order
import logging

logger = logging.getLogger("error_logger")

__all__ = [
    "notify_superadmin_new_order",
    "notify_superadmin_new_order_batch",
]


@shared_task(name="notify_superadmin_new_order")
def notify_superadmin_new_order(order_id):
    try:
        order = Order.objects.get(pk=order_id)
        context = {
            "subject": "[PinGo Mall]新規注文がありました",
            "type": "新規注文",
            "content": "新規注文が入りました。ご確認・対応をお願いいたします。",

            "order_id": order.id,
            "username": order.user.username,
            "quantity": order.Qty,
            "total": order.Total,

            "button_blue_text": f"ログイン",
            "button_blue_url": f"https://www.pingo.jp/backend/account/login",
            "button_grey_text": None,
            "button_grey_url": None,
        }
        pingo_settings.EMAIL.superadmin_new_order_notification(context=context).send([pingo_settings.ADMIN_EMAIL])
    except Exception as err:
        logger.error(PrintExceptionError(err))


@shared_task(name="notify_superadmin_new_order_batch")
def notify_superadmin_new_order_batch(order_ids):
    try:
        for order_id in order_ids:
            notify_superadmin_new_order(order_id)
    except Exception as err:
        logger.error(PrintExceptionError(err))
