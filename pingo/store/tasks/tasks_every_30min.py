from celery import shared_task
from celery.decorators import periodic_task
from celery.task.schedules import crontab
from django.db.models import Sum, F
from store.models import ViewProductHistory, Variation, InventoryHistory, Order, OrderItem, Margin, PingoItem
from core.functions import PrintExceptionError
from pingo.conf import settings as pingo_settings
from django.core import management
from django.core.cache import cache
import logging

logger = logging.getLogger("error_logger")

__all__ = [
    "update_latest_variation_stock",
    "rebuild_elasticsearch_indexing",
    "every_30_minutes_tasks",
]


@shared_task
def update_latest_variation_stock():
    variations = Variation.objects.all()

    if variations.count():
        for variation in variations:
            stock_sum = InventoryHistory.objects.filter(variation=variation).aggregate(
                total=Sum(F("quantity") * F("in_out")))

            if variation.inventory != stock_sum["total"]:
                logger.error("update variation inventory")
                logger.error(
                    f"variationID:{variation.id}, before: {variation.inventory}, updating:{stock_sum['total']}")
                variation.inventory = stock_sum["total"] if stock_sum["total"] is not None else 0
                variation.save()

                product_keys = pingo_settings.REDIS_KEYS["PRODUCT"].format(
                    variation.item.id)
                cache.delete_pattern(f"*{product_keys}*")


@shared_task
def rebuild_elasticsearch_indexing():
    print("rebuild_elasticsearch_indexing")
    management.call_command('search_index', '--rebuild', '-f')
    update_latest_variation_stock.delay()


@periodic_task(run_every=(crontab(minute='*/30')))
def every_30_minutes_tasks():
    update_latest_variation_stock.delay()
    rebuild_elasticsearch_indexing.delay()
