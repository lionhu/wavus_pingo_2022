from django.db import models
from django.conf import settings
from jsonfield import JSONField
from store.models import RegularManager, PingoItem
import uuid
import logging

logger = logging.getLogger("error_logger")

__all__ = [
    "AddressBook",
    "Logistic",

    "Order",
    "OrderItem",
    "PingoOrder",

    "default_delivery_info",
    "default_orderitem_payment_info",
]


def default_orderitem_payment_info():
    return {
        "method": "bank transfer"
    }
def default_delivery_info():
    return {
        "logistic_name": "",
        "track_no": "",
        "track_link": "",
    }


class AddressBook(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="shippingaddress",
                             blank=True, null=True)
    name = models.CharField(max_length=56)
    email = models.EmailField(max_length=128)
    phone = models.CharField(max_length=56)
    postcode = models.CharField(max_length=20)
    state = models.CharField(max_length=56)
    town = models.CharField(max_length=56)
    city = models.CharField(max_length=128)
    address_1 = models.CharField(max_length=256)
    address_2 = models.CharField(max_length=256, blank=True, null=True)

    def __str__(self):
        return "{}, {}".format(self.name, self.postcode)


class Logistic(models.Model):
    LOGISTIC_COMPANIES = (
        ("yamato", "クロネコヤマト"),
        ("sagawa", "佐川急便"),
        ("jppost_pack", "ゆうパック"),
        ("jppost_mail", "郵便書留"),
        ("seino", "西濃運輸"),
        ("seibu", "西武運輸"),
        ("fukutsu", "福山通運"),
        ("nittsu_air", "日通航空"),
        ("ems", "EMS"),
        ("dhl", "DHL"),
        ("ups", "UPS"),
        ("fedex", "FedEx"),
        ("wavus", "Wavus"),
        ("others", "Others"),
    )

    company = models.CharField(max_length=64, default="クロネコヤマト")
    short_name = models.CharField(
        max_length=32, default="yamato", choices=LOGISTIC_COMPANIES)
    is_valid = models.BooleanField(default=True, )
    track_link = models.CharField(max_length=256, default="")

    def __str__(self):
        return self.company


class Order(models.Model):
    ORDER_STATUS = (
        ("NEW", "NEW"),
        ("PROCESSING", "PROCESSING"),
        ("DELIVERING", "DELIVERING"),
        ("FINISHED", "FINISHED"),
    )

    ORDER_PAYMENT_METHOD = (
        ("CARD", "CARD"),
        ("POINT", "POINT"),
        ("MIX", "MIX"),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name="orders")
    slug = models.UUIDField(default=uuid.uuid4, unique=True)
    type = models.CharField(default="REGULAR", max_length=10)
    status = models.CharField(choices=ORDER_STATUS,
                              max_length=10, default="NEW")
    supplier_paid = models.BooleanField(blank=True, null=True, default=False)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_at = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False)
    is_valid = models.BooleanField(default=False)
    cart_items = JSONField(default=dict)
    json_shippingaddress = JSONField(default=dict)
    Qty = models.IntegerField(default=0)
    Total = models.IntegerField(default=0)
    chargeAmount = models.IntegerField(default=0)

    point_usage = JSONField(blank=True, null=True, default=dict)
    order_bonus = JSONField(blank=True, null=True, default=dict)

    message = models.TextField(blank=True, null=True, default="")
    is_paid = models.BooleanField(default=False)
    payment_method = models.CharField(
        choices=ORDER_PAYMENT_METHOD, max_length=20, default="CARD")
    payment_status = models.CharField(
        max_length=20, blank=True, null=True, default="")
    payment_id = models.CharField(
        max_length=128, blank=True, null=True, default="")
    payment_info = JSONField(blank=True, null=True, default=dict)

    is_delivered = models.BooleanField(blank=True, null=True, default=False)
    delivered_at = models.DateTimeField(blank=True, null=True)
    delivery_info = JSONField(blank=True, null=True,
                              default=default_delivery_info)
    logistic = models.ForeignKey(
        Logistic, blank=True, null=True, on_delete=models.SET_NULL, related_name="orders")


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
    regular_objects = RegularManager()

    def __str__(self):
        return "{}'s order".format(self.user.username)

    @property
    def total(self):
        total_purchase_price = 0
        total_price = 0
        profit = 0
        for order_item in self.orderitems.all():
            total_purchase_price += order_item.total_purchase_price
            total_price += order_item.total_price
            profit += order_item.profit
        return {
            "total_price": total_price,
            "total_purchase_price": total_purchase_price,
            "profit": profit,
        }


class OrderItem(models.Model):
    order = models.ForeignKey("Order",
                              on_delete=models.CASCADE, related_name="orderitems")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE,
                             related_name="orderitems")

    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(
        "Item", on_delete=models.CASCADE, related_name="orderitems")
    variation = models.ForeignKey(
        "Variation", on_delete=models.CASCADE, related_name="orderitems")

    quantity = models.IntegerField(default=1)
    final_price = models.IntegerField(null=True, blank=True)
    status = models.CharField(null=True, blank=True,
                              default="NEW", max_length=32)

    def __str__(self):
        return f"{self.quantity} of {self.item.item_name}"

    @property
    def total_price(self):
        return self.quantity * self.variation.price

    @property
    def total_purchase_price(self):
        return self.quantity * self.variation.purchase_price

    @property
    def profit(self):
        return self.total_price - self.total_purchase_price


class PingoOrder(models.Model):
    ORDER_PAYMENT_METHOD = (
        ("CARD", "CARD"),
        ("POINT", "POINT"),
        ("MIX", "MIX"),
    )
    slug = models.UUIDField(default=uuid.uuid4, unique=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="pingo_orders")
    product = models.ForeignKey(
        PingoItem, on_delete=models.CASCADE, blank=True, null=True, related_name="orders")
    quantity = models.IntegerField(default=1)
    price = models.IntegerField(default=0)
    total = models.IntegerField(blank=True, null=True, default=0)
    chargeAmount = models.IntegerField(blank=True, null=True, default=0)

    status = models.CharField(default="RECRUITING", max_length=28)
    is_paid = models.BooleanField(default=False)
    point_usage = JSONField(blank=True, null=True, default=dict)
    payment_method = models.CharField(
        choices=ORDER_PAYMENT_METHOD, max_length=20, default="CARD")
    payment_status = models.CharField(
        max_length=20, blank=True, null=True, default="")
    payment_id = models.CharField(
        max_length=128, blank=True, null=True, default="")
    payment_info = JSONField(blank=True, null=True, default=dict)

    json_shippingaddress = JSONField(blank=True, null=True, default=None)
    json_product = JSONField(blank=True, null=True, default=None)
    message = models.TextField(blank=True, null=True)

    delivered = models.BooleanField(blank=True, null=True, default=False)
    delivered_at = models.DateTimeField(blank=True, null=True)
    delivery_info = JSONField(blank=True, null=True,
                              default=default_delivery_info)
    logistic = models.ForeignKey(
        Logistic, blank=True, null=True, on_delete=models.SET_NULL)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}, product: {}".format(self.user.username, self.product.item_name)
