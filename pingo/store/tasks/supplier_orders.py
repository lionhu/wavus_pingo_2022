from celery import shared_task
from core.functions import PrintExceptionError
from pingo.conf import settings as pingo_settings
from store.models import OrderItem
import logging

logger = logging.getLogger("error_logger")

__all__ = [
    "notify_supplier_orderitem",
    "notify_supplier_orderitem_batch",
]


@shared_task(name="notify_supplier_orderitem")
def notify_supplier_orderitem(orderitem_id):
    try:
        orderitem = OrderItem.objects.get(pk=orderitem_id)
        supplier = orderitem.item.supplier
        context = {
            "subject": "[PinGo Mall]新規注文がありました",
            "type": "新規注文",
            "content": "新規注文が入りました。ご確認・対応をお願いいたします。",

            "orderitem_id": orderitem.id,
            "username": orderitem.user.username,
            "item_name": orderitem.item.item_name,
            "variation_name": orderitem.variation.name,
            "quantity": orderitem.quantity,

            "button_blue_text": f"ログイン",
            "button_blue_url": f"https://www.pingo.jp/backend/account/login",
            "button_grey_text": None,
            "button_grey_url": None,
        }
        pingo_settings.EMAIL.supplier_new_orderitem_notification(context=context).send([supplier.email])
    except Exception as err:
        logger.error(PrintExceptionError(err))


@shared_task(name="notify_supplier_orderitem_batch")
def notify_supplier_orderitem_batch(orderitem_ids):

    try:
        for orderitem_id in orderitem_ids:
            notify_supplier_orderitem(orderitem_id)
    except Exception as err:
        logger.error(PrintExceptionError(err))



