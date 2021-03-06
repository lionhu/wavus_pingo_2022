from django.db import models
from django.conf import settings
from jsonfield import JSONField
from mptt.models import MPTTModel, TreeForeignKey
from django.db.models import Min, Sum
from django.utils.timezone import make_aware
import uuid
import os
from datetime import datetime, timedelta
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from pingo.conf import settings as pingo_settings
from django.utils import timezone
import logging

logger = logging.getLogger("error_logger")

__all__ = [
    "Category",
    "Section",
    "Faq",
    "Supplier",
    "Item",
    "ItemSliderImage",
    "PingoItem",
    "PingoItemSliderImage",
    "Variation",
    "Favorite",
    "Comment",
    "Thumbs",
    "ViewProductHistory",
    "InventoryHistory",
    "Margin",
    "PointBank",
    "RegularManager",
    "BaseImageModel",
    "Baseitem",

    "image_path",
    "default_point_rule",
    "empty_json",
    "point_expired_date",
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
