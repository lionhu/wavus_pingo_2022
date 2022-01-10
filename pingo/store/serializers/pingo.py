from rest_framework import serializers
from rest_flex_fields import FlexFieldsModelSerializer
from store.models import Category, Faq, Section, Logistic, Supplier, AddressBook, Item, \
    ItemSliderImage, Variation, ViewProductHistory, Comment, Thumbs, Favorite, \
    OrderItem, InventoryHistory, Order, PointBank, Margin, PingoItem, PingoOrder, \
    PingoItemSliderImage
from store.serializers import SupplierSerializer, LogisticSerializer
from rolepermissions.checkers import has_role
from authentication.serializers import PingoUserSerializer
import logging

logger = logging.getLogger("error_logger")

__all__ = [
    "PingoItemSliderImageSerializer",
    "PingoItemSerializer",
    "PingoOrderSerializer",
]


class PingoItemSliderImageSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = PingoItemSliderImage
        fields = ("id", "item", "image", "is_valid", "title", "http_referer", "type", "image_url", "thumbimage_url",)


class PingoItemSerializer(FlexFieldsModelSerializer):
    labels = serializers.JSONField()
    point_rule = serializers.JSONField()

    class Meta:
        model = PingoItem
        fields = ("id", "item_name", "sort_by", "supplier", "brand", "series", "model", "category", "package",
                  "is_valid", "rate", "item_pingo_sliderimages", "video_url", "labels", "description", "status",
                  "targetNum", "currentNum", "until_at", "image_url",
                  "price", "discount_price", "purchase_price", "point_rule", "thumbimage_url", "created_at")
        expandable_fields = {
            "item_pingo_sliderimages": (PingoItemSliderImageSerializer, {"many": True, "required": False}),
            "supplier": (SupplierSerializer, {"many": False, "required": False}),
        }
        private_fields = ("purchase_price",)

    def __init__(self, *args, **kwargs):
        # Instantiate the superclass normally
        super(PingoItemSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request', None)

        if request is None or not has_role(request.user, ["superadmin", "staff", "supplier"]):
            if hasattr(self.Meta, "private_fields") and len(self.Meta.private_fields) > 0:
                for field_name in self.Meta.private_fields:
                    self.fields.pop(field_name)


class PingoOrderSerializer(FlexFieldsModelSerializer):
    json_shippingaddress = serializers.JSONField()
    json_product = serializers.JSONField()
    point_usage = serializers.JSONField()
    delivery_info = serializers.JSONField(required=False)
    payment_info = serializers.JSONField(required=False)

    class Meta:
        model = PingoOrder
        fields = (
            'id', 'user', "slug", "product", "json_product", 'quantity', "price", "total", "chargeAmount", "status",
            "is_paid", "point_usage", "payment_status", "payment_method", "payment_id",
            "payment_info", "json_shippingaddress", "message", "created_at",
            "delivered", "delivered_at", "delivery_info", "logistic",
            "updated_at",)
        expandable_fields = {
            "product": (PingoItemSerializer, {"many": False}),
            "user": (PingoUserSerializer, {"many": False}),
            "logistic": (LogisticSerializer, {"many": False}),
        }
