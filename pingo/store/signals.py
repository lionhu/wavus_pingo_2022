from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.dispatch import Signal
from django.db.models import Sum, F
from django.core.cache import cache
from core.functions import remove_image_file, suqre_crop_image
from pingo.conf import settings as pingo_settings
from store.models import OrderItem, InventoryHistory, PingoOrder
import os
import logging

logger = logging.getLogger("error_logger")

signalOrderItemStatusChanged = Signal(providing_args=["orderitem"])
signalOrderItemSupplierPaymentChanged = Signal(providing_args=["orderitem"])


def update_variation_stock(variation):
    _sum = InventoryHistory.objects.filter(variation=variation).aggregate(
        total=Sum(F("quantity") * F("in_out")))
    logger.error(_sum)
    variation.inventory = _sum["total"]
    variation.save()


def update_pingo_currentNum(pingo_product):
    pingoitem_currentNum = PingoOrder.objects.filter(product=pingo_product).aggregate(quantity=Sum('quantity'))[
        "quantity"]
    pingo_product.currentNum = pingoitem_currentNum if pingoitem_currentNum is not None else 0
    logger.error("signalPingoProductCurrentChanged currentNum:{}".format(pingoitem_currentNum))
    if pingo_product.currentNum >= pingo_product.targetNum:
        pingo_product.status = "ESTABLISHED"
    pingo_product.save()


@receiver(signalOrderItemStatusChanged)
def orderitem_status_changed(sender, **kwargs):
    # orderitem is sender
    status = kwargs["status"]
    order = sender.order
    if status == "PROCESSING":
        order.status = "PROCESSING"
        logger.error("set order status to PROCESSING")
        order.save()
        return order

    if status == "DELIVERING":
        orderitems = order.orderitems.all()
        delivery_count = 0
        for item in orderitems:
            if item.status == status:
                delivery_count += 1

        if len(orderitems) == delivery_count:
            order.status = status
            logger.error("set order status to PROCESSING")
            order.save()
            return order


@receiver(signalOrderItemSupplierPaymentChanged)
def orderitem_supplier_payment_changed(sender, **kwargs):
    # orderitem is sender
    orderitems = OrderItem.objects.filter(order=sender.order)
    paid = True
    for item in orderitems:
        if not item.paid:
            paid = False
            break

    sender.order.supplier_paid = paid
    logger.error(f"set order supplier_paid to {paid}")
    sender.order.save()


@receiver(post_delete)
def after_delete_store_object(sender, instance, **kwargs):
    app_label = sender._meta.app_label
    model_name = sender._meta.model_name

    if app_label == "store":
        if model_name in ["item", "itemsliderimage", "pingoitem", "pingoitemsliderimage", "variation"]:
            if instance.id is not None:
                if hasattr(instance, "thumbimage") and str(instance.image) != pingo_settings.DEFAULT_IMAGE:
                    remove_image_file(instance.thumbimage, True)

                if instance.image != pingo_settings.DEFAULT_IMAGE:
                    remove_image_file(instance.image)

        if model_name == "orderitem":
            if instance.id is not None:
                if instance.quantity > 0 and instance.variation is not None:
                    logger.error(f"Delete Before instance.variation.inventory", instance.variation.inventory)
                    inventory = InventoryHistory.objects.create(
                        variation=instance.variation,
                        type="OC",
                        in_out=1,
                        quantity=instance.quantity,
                        info={
                            "order": instance.order.id,
                            "orderitem": instance.id,
                            "user_id": instance.order.user.id,
                            "username": instance.order.user.username
                        })
                    # update_variation_stock(instance.variation)
                    # sum = InventoryHistory.objects.filter(variation=instance.variation).aggregate(
                    #     total=Sum(F("quantity") * F("in_out")))
                    # instance.variation.inventory = sum["total"]
                    # instance.variation.save()
                    logger.error(f"After instance.variation.inventory", instance.variation.inventory)

        if model_name == "pingoorder":
            update_pingo_currentNum(instance.product)


@receiver(pre_save)
def before_save_store_object(sender, instance, **kwargs):
    app_label = sender._meta.app_label
    model_name = sender._meta.model_name

    logger.error(f"{app_label}-{model_name}")

    if app_label == "store":
        if model_name in ["item", "itemsliderimage", "pingoitem", "pingoitemsliderimage", "variation"]:
            if instance.id is None:
                instance.image = suqre_crop_image(instance.image, 'foo.jpg')
                logger.error("pre_save instance.id: None, suqre_crop_image for new item")
            else:

                filename = os.path.basename(instance.image.path)
                existing_item = sender.objects.filter(pk=instance.id).first()
                existing_filename = os.path.basename(existing_item.image.path)
                logger.error(
                    f"pre_save instance.id: {instance.id}, instance.filename: {filename}, existing_filename: {existing_filename}")

                if existing_filename == pingo_settings.DEFAULT_IMAGE:
                    instance.image = suqre_crop_image(instance.image, 'foo.jpg')
                elif filename != existing_filename:
                    remove_image_file(existing_item.image)
                    remove_image_file(existing_item.thumbimage, True)
                    logger.error(f"removed existing imagefiles: {existing_filename}")
                    instance.image = suqre_crop_image(instance.image, 'foo.jpg')
                    logger.error("suqre_crop_image for update")
                # else:
                #     logger.error("doing nothing with image update or crop")

        if model_name == "orderitem":
            if instance.id is None:
                if instance.quantity > 0 and instance.variation is not None:
                    InventoryHistory.objects.create(
                        variation=instance.variation,
                        type="OU",
                        in_out=-1,
                        quantity=instance.quantity,
                        info={
                            "order": instance.order.id,
                            "orderitem": instance.id,
                            "user_id": instance.order.user.id,
                            "username": instance.order.user.username
                        })
            else:
                old_orderitem = OrderItem.objects.filter(pk=instance.id).first()
                if old_orderitem is not None and old_orderitem.quantity != instance.quantity:
                    InventoryHistory.objects.create(
                        variation=instance.variation,
                        type="OC",
                        in_out=1,
                        quantity=old_orderitem.quantity,
                        info={
                            "order": instance.order.id,
                            "orderitem": instance.id,
                            "user_id": instance.order.user.id,
                            "username": instance.order.user.username
                        })
                    InventoryHistory.objects.create(
                        variation=instance.variation,
                        type="OU",
                        in_out=-1,
                        quantity=instance.quantity,
                        info={
                            "order": instance.order.id,
                            "orderitem": instance.id,
                            "user_id": instance.order.user.id,
                            "username": instance.order.user.username
                        })
            cache.delete_pattern(f"*_product*")


@receiver(post_save)
def after_save_store_object(sender, instance, created, **kwargs):
    app_label = sender._meta.app_label
    model_name = sender._meta.model_name

    if app_label == "store":
        if model_name == "inventoryhistory":
            update_variation_stock(instance.variation)
            product_key = pingo_settings.REDIS_KEYS["PRODUCT"].format(instance.variation.item.id)
            category_products_key = pingo_settings.REDIS_KEYS["CATEGORY_PRODUCTS"].format(
                instance.variation.item.category.id)
            cache.delete_pattern(f"*{product_key}*")
            cache.delete_pattern(f"*{category_products_key}*")
            # cache.delete_pattern(f"*_product*")

        if model_name == "pingoorder":
            update_pingo_currentNum(instance.product)
