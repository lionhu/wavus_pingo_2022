from celery import shared_task
from celery.decorators import periodic_task
from celery.task.schedules import crontab
from store.models import ViewProductHistory, Variation, InventoryHistory, Order, OrderItem, Margin, PingoItem
from datetime import datetime
from django.utils.timezone import make_aware
import logging

logger = logging.getLogger("error_logger")

__all__ = [
    "update_pingo_status",
    "every_minute_tasks",
]


@shared_task
def update_pingo_status():
    aware_time = make_aware(datetime.now())
    filters = {
        "is_valid": True,
        "status": "RECRUITING",
        "until_at__lte": aware_time,
    }

    pingo_items = PingoItem.objects.filter(**filters)
    if pingo_items.exists():
        for item in pingo_items:
            if item.currentNum >= item.targetNum:
                item.status = "ESTABLISHED"
                item.save()
            else:
                item.status = "PROCESSING"
                item.save()


@periodic_task(run_every=(crontab()))
def every_minute_tasks():
    update_pingo_status.delay()
