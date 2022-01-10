from django.db import models
from django.conf import settings
from jsonfield import JSONField
from mptt.models import MPTTModel, TreeForeignKey
from django.db.models import Min, Sum
from django.utils.timezone import make_aware
import uuid
import json
import os
from datetime import datetime, timedelta
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from pingo.conf import settings as pingo_settings
from django.utils import timezone
import logging

logger = logging.getLogger("error_logger")

__all__ = [
    "AddressBook",
    "Category",
    "Logistic",
    "Section",
    "Faq",
    "Supplier",
    "Item",
    "ItemSliderImage",
    "PingoItem",
    "PingoItemSliderImage",
    "PingoOrder",
    "Variation",
    "Favorite",
    "Comment",
    "Thumbs",
    "ViewProductHistory",
    "InventoryHistory",
    "Order",
    "OrderItem",
    "Margin",
    "PointBank",
    "RegularManager",
    "BaseImageModel",
    "Baseitem",

    "image_path",
    "default_point_rule",
    "default_delivery_info",
    "empty_json",
    "point_expired_date",
    "default_orderitem_payment_info",
]


def image_path(instance, filename):
    extension = filename.split(".")[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex[:10], extension.lower())
    file_path = os.path.join("product", "images", filename.lower())
    return file_path


def default_point_rule():
    return {
        "is_valid": False,
        "type": "amount",
        "policies": {
            "level_1": 0,
            "level_2": 0,
            "client_admin": 0,
            "client_superadmin": 0,
        }
    }


def empty_json():
    return {}


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


class Category(MPTTModel):
    default_menu_access_right = {
        "superadmin": True,
        "supplier": False,
        "client_admin": False
    }
    default_menu_badge = {
        "variant": "success",
        "text": "menuitems.dashboard.badge"
    }
    title = models.CharField(max_length=64, default="label")
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    is_valid = models.BooleanField(default=False)
    isTitle = models.BooleanField(default=True)
    isMenuCollapsed = models.BooleanField(default=True)
    access = JSONField(blank=True, null=True, default=default_menu_access_right)
    icon = models.CharField(max_length=128, blank=True, null=True, default="ri-dashboard-line")
    badge = JSONField(blank=True, null=True, default=default_menu_badge)
    link = models.CharField(max_length=128, blank=True, null=True, default="/")
    sort_by = models.IntegerField(default=0)

    class MPTTMeta:
        order_insertion_by = ['title']

    def __str__(self):
        return "{}".format(self.title)

    @property
    def pingo_product_count(self):
        sub_cats = self.get_descendants(include_self=True)
        aware_time = make_aware(datetime.now())
        return PingoItem.objects.filter(category__in=sub_cats, is_valid=True, status="RECRUITING",
                                        until_at__gte=aware_time).count()

    @property
    def regular_product_count(self):
        sub_cats = self.get_descendants(include_self=True)
        return Item.regular_objects.filter(category__in=sub_cats, is_valid=True).count()


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
    short_name = models.CharField(max_length=32, default="yamato", choices=LOGISTIC_COMPANIES)
    is_valid = models.BooleanField(default=True, )
    track_link = models.CharField(max_length=256, default="")

    def __str__(self):
        return self.company


class Section(models.Model):
    title = models.CharField(max_length=64, default="section")
    index = models.IntegerField(default=0)
    is_valid = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Faq(models.Model):
    question = models.CharField(max_length=100, default="section")
    index = models.IntegerField(default=0)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name="faqs")
    answer = models.TextField(default="", )
    is_valid = models.BooleanField(default=False)

    def __str__(self):
        return self.question


class Supplier(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name="supplier")
    name = models.CharField(max_length=64)
    email = models.EmailField(max_length=128, null=True, blank=True, )
    website = models.CharField(max_length=256, null=True, blank=True, default="")
    phone = models.CharField(max_length=32, default="")
    postcode = models.CharField(max_length=20, default="")
    state = models.CharField(max_length=64, default="")
    city = models.CharField(max_length=64, default="")
    town = models.CharField(max_length=64, default="")
    address_1 = models.CharField(max_length=128, default="")
    address_2 = models.CharField(max_length=128, default="")
    is_valid = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class RegularManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(type="REGULAR").order_by("-sort_by")

    def get_valid_queryset(self):
        return super().get_queryset().filter(type="REGULAR", **pingo_settings.VALID_PRODUCT_LOOKUP).order_by("-sort_by")


class BaseImageModel(models.Model):
    image = models.ImageField(null=True, blank=True, default="default.jpg", upload_to=image_path)
    thumbimage = ImageSpecField(
        source='image',
        processors=[ResizeToFill(256, 256)],
        format='JPEG',
        options={'quality': 95}
    )

    class Meta:
        abstract = True


class Item(BaseImageModel):
    PRODUCT_TYPE = (
        ('REGULAR', 'Regular'),
        ('PINGO', 'Pingo')
    )

    item_name = models.CharField(max_length=100, default="_item_name_")
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True, blank=True, default=None,
                                 related_name="supplier_items")
    brand = models.CharField(max_length=50, null=True, blank=True, default="")
    series = models.CharField(max_length=50, null=True, blank=True, default="")
    model = models.CharField(max_length=50, null=True, blank=True, default="")
    type = models.CharField(choices=PRODUCT_TYPE, default="REGULAR", max_length=10)
    sort_by = models.IntegerField(default=0)

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category_items")
    labels = JSONField(blank=True, null=True, default=dict)

    description = models.TextField(null=True, blank=True, default="")
    package = models.TextField(null=True, blank=True, default="")
    rate = models.IntegerField(default=5)
    video_url = models.CharField(default="", max_length=256)
    is_valid = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
    regular_objects = RegularManager()

    def __str__(self):
        return self.item_name

    @property
    def image_url(self):
        return "{}{}".format(pingo_settings.NICHIEI_INFO["WEBSITE"], self.image.url)

    @property
    def thumbimage_url(self):
        return "{}{}".format(pingo_settings.NICHIEI_INFO["WEBSITE"], self.thumbimage.url)

    @property
    def supplier_indexing(self):
        return self.supplier.name if self.supplier is not None else ""

    @property
    def category_indexing(self):
        return self.category.title

    @property
    def variation_min_price(self):
        result = Variation.objects.filter(item=self).aggregate(min_price=Min("price"))
        if result["min_price"] is None:
            return 0
        return result["min_price"]

    @property
    def variation_stock_total(self):
        result = Variation.objects.filter(item=self).aggregate(total_stock=Sum("inventory"))
        if result["total_stock"] is None:
            return 0
        return result["total_stock"]


class ItemSliderImage(BaseImageModel):
    is_valid = models.BooleanField(default=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="item_sliderimages")
    title = models.CharField(max_length=100, blank=True, null=True, default="item_sliderimage")
    http_referer = models.CharField(max_length=256, blank=True, null=True, default="")
    type = models.CharField(max_length=100, blank=True, null=True, default="")
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def image_url(self):
        return "{}{}".format(pingo_settings.NICHIEI_INFO["WEBSITE"], self.image.url)

    @property
    def thumbimage_url(self):
        return "{}{}".format(pingo_settings.NICHIEI_INFO["WEBSITE"], self.thumbimage.url)


class PingoItem(BaseImageModel):
    PINGOITEM_STATUS = (
        ("RECRUITING", "RECRUITING"),
        ("PROCESSING", "PROCESSING"),
        ("ESTABLISHED", "ESTABLISHED"),
        ("RELEASED", "RELEASED"),
    )

    item_name = models.CharField(max_length=100, default="_item_name_")
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True, blank=True, default=None,
                                 related_name="supplier_pingo_items")
    brand = models.CharField(max_length=50, null=True, blank=True, default="")
    series = models.CharField(max_length=50, null=True, blank=True, default="")
    model = models.CharField(max_length=50, null=True, blank=True, default="")
    sort_by = models.IntegerField(default=0)

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category_pingo_items")
    labels = JSONField(blank=True, null=True, default=dict)

    description = models.TextField(null=True, blank=True, default="")
    package = models.TextField(null=True, blank=True, default="")
    rate = models.IntegerField(default=5)
    video_url = models.CharField(default="", null=True, blank=True, max_length=256)
    is_valid = models.BooleanField(default=False)

    status = models.CharField(choices=PINGOITEM_STATUS, default="RECRUITING", max_length=28)
    targetNum = models.IntegerField(default=1)
    currentNum = models.IntegerField(default=0)
    until_at = models.DateTimeField(default=timezone.now)

    price = models.IntegerField(default=0)
    discount_price = models.IntegerField(default=0)
    purchase_price = models.IntegerField(default=0)

    point_rule = JSONField(blank=True, null=True, default=default_point_rule)

    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    def __str__(self):
        return "{},targetNum:{}".format(self.item_name, self.targetNum)

    @property
    def image_url(self):
        return "{}{}".format(pingo_settings.NICHIEI_INFO["WEBSITE"], self.image.url)

    @property
    def thumbimage_url(self):
        return "{}{}".format(pingo_settings.NICHIEI_INFO["WEBSITE"], self.thumbimage.url)


class PingoItemSliderImage(BaseImageModel):
    is_valid = models.BooleanField(default=True)
    item = models.ForeignKey(PingoItem, on_delete=models.CASCADE, related_name="item_pingo_sliderimages")
    title = models.CharField(max_length=100, blank=True, null=True, default="item_sliderimage")
    http_referer = models.CharField(max_length=256, blank=True, null=True, default="")
    type = models.CharField(max_length=100, blank=True, null=True, default="")
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title

    @property
    def image_url(self):
        return "{}{}".format(pingo_settings.NICHIEI_INFO["WEBSITE"], self.image.url)

    @property
    def thumbimage_url(self):
        return "{}{}".format(pingo_settings.NICHIEI_INFO["WEBSITE"], self.thumbimage.url)


def default_delivery_info():
    return {
        "logistic_name": "",
        "track_no": "",
        "track_link": "",
    }


class PingoOrder(models.Model):
    ORDER_PAYMENT_METHOD = (
        ("CARD", "CARD"),
        ("POINT", "POINT"),
        ("MIX", "MIX"),
    )
    slug = models.UUIDField(default=uuid.uuid4, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="pingo_orders")
    product = models.ForeignKey(PingoItem, on_delete=models.CASCADE, blank=True, null=True, related_name="orders")
    quantity = models.IntegerField(default=1)
    price = models.IntegerField(default=0)
    total = models.IntegerField(blank=True, null=True, default=0)
    chargeAmount = models.IntegerField(blank=True, null=True, default=0)

    status = models.CharField(default="RECRUITING", max_length=28)
    is_paid = models.BooleanField(default=False)
    point_usage = JSONField(blank=True, null=True, default=dict)
    payment_method = models.CharField(choices=ORDER_PAYMENT_METHOD, max_length=20, default="CARD")
    payment_status = models.CharField(max_length=20, blank=True, null=True, default="")
    payment_id = models.CharField(max_length=128, blank=True, null=True, default="")
    payment_info = JSONField(blank=True, null=True, default=dict)

    json_shippingaddress = JSONField(blank=True, null=True, default=None)
    json_product = JSONField(blank=True, null=True, default=None)
    message = models.TextField(blank=True, null=True)

    delivered = models.BooleanField(blank=True, null=True, default=False)
    delivered_at = models.DateTimeField(blank=True, null=True)
    delivery_info = JSONField(blank=True, null=True, default=default_delivery_info)
    logistic = models.ForeignKey(Logistic, blank=True, null=True, on_delete=models.SET_NULL)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}, product: {}".format(self.user.username, self.product.item_name)


# base item for variation and options
class Baseitem(BaseImageModel):
    is_valid = models.BooleanField(default=False)
    name = models.CharField(max_length=100, blank=True, null=True, default="_variation")
    description = models.CharField(max_length=100, blank=True, null=True, default="")
    price = models.IntegerField(default=0)
    purchase_price = models.IntegerField(default=0)
    extra_cost = models.IntegerField(default=0)
    inventory = models.IntegerField(default=0)
    sku = models.CharField(null=True, blank=True, max_length=128)
    sort_by = models.IntegerField(default=0)
    point_rule = JSONField(blank=True, null=True, default=default_point_rule)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name

    @property
    def image_url(self):
        return "{}{}".format(pingo_settings.NICHIEI_INFO["WEBSITE"], self.image.url)

    @property
    def thumbimage_url(self):
        return "{}{}".format(pingo_settings.NICHIEI_INFO["WEBSITE"], self.thumbimage.url)

    @property
    def point_rule_indexing(self):
        return json.dumps(self.point_rule)

class Variation(Baseitem):
    PRODUCT_TYPE = (
        ('REGULAR', 'Regular'),
        ('PINGO', 'Pingo')
    )

    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='item_variations')
    variation_type = models.CharField(choices=PRODUCT_TYPE, default="REGULAR", max_length=10)
    type = models.CharField(max_length=50, default="COLOR")

    class Meta:
        ordering = ('price',)

    def __str__(self):
        return "{}-{}".format(self.type, self.name)



class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_favorites")
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="item_favorites")
    metadata = JSONField(blank=True, null=True, default=dict)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return "{}'s favorite item: {}".format(self.user.username, self.item.item_name)


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_comments")
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="item_comments")
    item_type = models.CharField(max_length=10, default="REGULAR")
    content = models.TextField(default="")
    rate = models.IntegerField(default=5)
    thumbs_up = models.IntegerField(default=0)
    thumbs_down = models.IntegerField(default=0)
    approved = models.BooleanField(default=False)
    checked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return "{}'s comment on item: {}".format(self.user.username, self.item.item_name)


class Thumbs(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_thumbs")
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="comment_thumbs")
    thumb_type = models.CharField(max_length=10, default="up")
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return "user_username:{}, on comment_id:{}".format(self.user.username, self.comment.id)


class ViewProductHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="viewproducts")
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    type = models.CharField(max_length=16, null=True, blank=True, default="REGULAR")
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return "{}'s browsed item: {}".format(self.user.username, self.item.item_name)


class InventoryHistory(models.Model):
    inventory_opt_types = {
        ('OU', 'ORDER USED'),
        ('OC', 'ORDER CANCELLED'),
        ('BS', 'BUY STOCK'),
        ('RS', 'RETURN STOCK')
    }
    default_info = {
        "order_id": 0,
        "description": "",
    }
    variation = models.ForeignKey(Variation, on_delete=models.CASCADE, related_name="stock")

    type = models.CharField(max_length=28, choices=inventory_opt_types, default="OU")
    in_out = models.IntegerField(default=-1)
    quantity = models.IntegerField(default=1)

    info = JSONField(default=default_info)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "variation {} - type {} - quantity {} ".format(self.variation.id, self.type,
                                                              self.quantity)


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

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders")
    slug = models.UUIDField(default=uuid.uuid4, unique=True)
    type = models.CharField(default="REGULAR", max_length=10)
    status = models.CharField(choices=ORDER_STATUS, max_length=10, default="NEW")
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
    payment_method = models.CharField(choices=ORDER_PAYMENT_METHOD, max_length=20, default="CARD")
    payment_status = models.CharField(max_length=20, blank=True, null=True, default="")
    payment_id = models.CharField(max_length=128, blank=True, null=True, default="")
    payment_info = JSONField(blank=True, null=True, default=empty_json)

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


def default_delivery_info():
    return {
        "logistic_name": "",
        "track_no": "",
        "track_link": "",
    }


def default_orderitem_payment_info():
    return {
        "method": "bank transfer"
    }


class OrderItem(models.Model):
    order = models.ForeignKey("Order",
                              on_delete=models.CASCADE, related_name="orderitems")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE,
                             related_name="orderitems")

    ordered = models.BooleanField(default=False)
    item = models.ForeignKey("Item", on_delete=models.CASCADE, related_name="orderitems")
    variation = models.ForeignKey("Variation", on_delete=models.CASCADE, related_name="orderitems")

    quantity = models.IntegerField(default=1)
    final_price = models.IntegerField(null=True, blank=True)
    status = models.CharField(null=True, blank=True, default="NEW", max_length=32)

    delivered = models.BooleanField(blank=True, null=True, default=False)
    delivered_at = models.DateTimeField(blank=True, null=True)
    delivery_info = JSONField(blank=True, null=True, default=default_delivery_info)
    logistic = models.ForeignKey(Logistic, blank=True, null=True, on_delete=models.SET_NULL, related_name="orderitems")

    paid = models.BooleanField(blank=True, null=True, default=False)
    paid_at = models.DateTimeField(blank=True, null=True)
    paid_info = JSONField(blank=True, null=True, default=default_orderitem_payment_info)

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


class Margin(models.Model):
    type = models.CharField(max_length=28, null=True, blank=True, default="INTRODUCE_POINT")
    order_type = models.CharField(max_length=28, null=True, blank=True, default="REGULAR")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="margins")
    amount = models.IntegerField(default=0)
    is_valid = models.BooleanField(default=False)
    is_refound = models.IntegerField(default=-1)
    paid_at = models.DateTimeField(blank=True, null=True)
    info = JSONField(default=dict)
    from_orderID = models.IntegerField(default=0, blank=True, null=True)
    fromuser = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL,
                                 related_name="fromuser_margins", default=None)
    pointbank_saved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} points to {} from order {}".format(self.type, self.user.username, self.amount)


def point_expired_date():
    expire_date = datetime.now() + timedelta(days=pingo_settings.SHOP_SETTINGS["POINT_EXPIRE_DAYS"])
    return expire_date


class PointBank(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="validpointbank")
    margin = models.OneToOneField(Margin, null=True, blank=True, on_delete=models.SET_NULL, related_name="pointbank")
    point = models.IntegerField(default=0, null=True, blank=True)
    until_at = models.DateTimeField(default=point_expired_date)
    info = JSONField(default=dict)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return "{}'s point: {}, until_at:{}".format(self.user.username, self.point, self.until_at)

    @property
    def user_index(self):
        return self.user.username
