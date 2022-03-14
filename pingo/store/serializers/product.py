from rest_framework import serializers
from rest_flex_fields import FlexFieldsModelSerializer
from store.models import Category, Faq, Section, Logistic, Supplier, AddressBook, Item, \
    ItemSliderImage, Variation, ViewProductHistory, Comment, Thumbs, Favorite, \
    OrderItem, InventoryHistory, Order, PointBank, Margin, PingoItem, PingoOrder, \
    PingoItemSliderImage
from djoser.serializers import UserSerializer
from store.serializers import SupplierSerializer, CategorySerializer, LogisticSerializer, ContextFlexFieldsModelSerialier
from rolepermissions.checkers import has_role
from authentication.serializers import PingoUserSerializer
import logging

logger = logging.getLogger("error_logger")

__all__ = [
    "VariationSerializer",
    "ItemSliderImageSerializer",
    "ItemSerializer",
    "ItemFullSerializer",
    "ViewProductHistorySerializer",
    "CommentSerializer",
    "CommentFullSerializer",
    "ThumbsSerializer",
    "FavoriteSerializer",
    "VariationFullSerializer",
    # "OrderItemFULLSerializer",
    # "OrderSerializer",
    # "OrderItemSerializer",
    "InventorySerializer",
    "MarginSerializer",
    "PointBankSerializer",
]


class VariationSerializer(ContextFlexFieldsModelSerialier):
    point_rule = serializers.JSONField()

    class Meta:
        model = Variation
        fields = (
            "id", 'name', "description", "extra_cost", "is_valid", "price", "purchase_price", "inventory", "sku",
            "sort_by", "point_rule", "item", "variation_type", "type", "image", "image_url", "thumbimage_url")
        private_fields = ("purchase_price",  "extra_cost", )


class ItemSliderImageSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = ItemSliderImage
        fields = ("id", "item", "image", "is_valid", "title", "http_referer", "type", "image_url", "thumbimage_url",)
        read_only_fields = ("image_url", "thumbimage_url",)


class ItemSerializer(ContextFlexFieldsModelSerialier):
    labels = serializers.JSONField()
    item_variations = serializers.SerializerMethodField("get_item_variations_serializer")
    # supplier = SupplierSerializer(many=False)

    class Meta:
        model = Item
        fields = ("id", "item_name", "sort_by", "supplier", "brand", "type", "series", "model", "category", "package",
                  "image", "image_url", "is_valid", "rate", "video_url", "labels", "item_variations",
                  "description", "item_sliderimages", "thumbimage_url", "created_at",)
        read_only_fields = ("item_sliderimages", "item_variations", "image_url", "thumbimage_url",)
        expandable_fields = {
            # "item_variations": (VariationSerializer, {"many": True}),
            "item_sliderimages": (ItemSliderImageSerializer, {"many": True}),
            "supplier": (SupplierSerializer, {"many": False}),
            "category": (CategorySerializer, {"many": False}),
        }
        # private_fields = ("description",)

    def get_item_variations_serializer(self,obj):
        serializer_context = {'request': self.context.get('request')}
        variations = Variation.objects.all().filter(item=obj)
        serializer = VariationSerializer(
            variations, many=True, context=serializer_context)
        return serializer.data


class ItemFullSerializer(serializers.ModelSerializer):
    labels = serializers.JSONField()
    item_variations = serializers.SerializerMethodField(
        "get_item_variations_serializer")
    item_sliderimages = ItemSliderImageSerializer(many=True)
    supplier = SupplierSerializer(many=False)

    class Meta:
        model = Item
        fields = ("id", "item_name", "sort_by", "supplier", "brand", "type", "series", "model", "category", "package",
                  "image", "image_url", "is_valid", "rate", "video_url", "labels", "item_variations",
                  "description", "item_sliderimages", "thumbimage_url", "created_at",)
        read_only_fields = ("item_sliderimages", "item_variations", "supplier", "image_url", "thumbimage_url",)

    def get_item_variations_serializer(self, obj):
        serializer_context = {'request': self.context.get('request')}
        variations = Variation.objects.all().filter(item=obj)
        serializer = VariationSerializer(
            variations, many=True, context=serializer_context)
        return serializer.data

class ViewProductHistorySerializer(FlexFieldsModelSerializer):
    class Meta:
        model = ViewProductHistory
        fields = ("id", "user", "item", "type", "created_at",)
        expandable_fields = {
            "item": (ItemSerializer, {"many": False}),
            "user": (PingoUserSerializer, {"many": False}),
        }


class CommentSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Comment
        fields = (
            "id", "item", "user", "item_type", "content", "rate", "thumbs_up", "thumbs_down", "approved", "checked",
            "created_at",)
        read_only_fields = ("thumbs_up", "thumbs_down",)
        expandable_fields = {
            "item": (ItemSerializer, {"many": False}),
            "user": (PingoUserSerializer, {"many": False}),
        }


class CommentFullSerializer(FlexFieldsModelSerializer):
    item = ItemSerializer(many=False)
    user = PingoUserSerializer(many=False)

    class Meta:
        model = Comment
        fields = (
            "id", "item", "item_type", "user", "content", "rate", "thumbs_up", "thumbs_down", "approved", "checked",
            "created_at",)
        read_only_fields = ("thumbs_up", "thumbs_down",)


class ThumbsSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Thumbs
        fields = ("id", "user", "comment", "thumb_type", "created_at",)
        expandable_fields = {
            "comment": (CommentSerializer, {"many": False}),
            "user": (PingoUserSerializer, {"many": False}),
        }


class FavoriteSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Favorite
        fields = ("id", "item", "user")
        expandable_fields = {
            "item": (ItemSerializer, {"many": False}),
            "user": (PingoUserSerializer, {"many": False}),
        }


class VariationFullSerializer(FlexFieldsModelSerializer):
    point_rule = serializers.JSONField()
    private_fields = ("purchase_price",)
    item = ItemFullSerializer(many=False)

    class Meta:
        model = Variation
        fields = (
            "id", 'name', "description", "extra_cost", "is_valid", "price", "purchase_price", "inventory", "sku",
            "sort_by", "point_rule", "item", "variation_type", "type", "image", "image_url", "thumbimage_url")
        private_fields = ("purchase_price",)

    def __init__(self, *args, **kwargs):
        # Instantiate the superclass normally
        super(VariationFullSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request', None)

        if request is None or not has_role(request.user, ["superadmin", "staff", "supplier"]):
            if hasattr(self.Meta, "private_fields") and len(self.Meta.private_fields) > 0:
                for field_name in self.Meta.private_fields:
                    self.fields.pop(field_name)


class InventorySerializer(FlexFieldsModelSerializer):
    class Meta:
        model = InventoryHistory
        fields = ("id", "variation", "type", "in_out", "quantity", "info", "created_at",
                  )
        expandable_fields = {
            "variation": (VariationSerializer, {"many": False})
        }

    def __init__(self, *args, **kwargs):
        # Instantiate the superclass normally
        super(InventorySerializer, self).__init__(*args, **kwargs)

        private_fields = self.context.get('private_fields', None)
        logger.error("private_fields")
        logger.error(private_fields)
        if private_fields:
            fields = private_fields.split(',')
            not_allowed = set(fields)
            for field_name in not_allowed:
                self.fields.pop(field_name)


class MarginSerializer(FlexFieldsModelSerializer):
    fromuser = serializers.CharField(source="fromuser.username")
    info = serializers.JSONField()

    class Meta:
        model = Margin
        fields = ("id", "type", "amount", "order_type", "is_valid", "is_refound", "paid_at", "info",
                  "from_orderID", "pointbank_saved", "created_at", "user", "fromuser",)
        expandable_fields = {
            "user": (PingoUserSerializer, {"many": False})
        }


class PointBankSerializer(FlexFieldsModelSerializer):
    info = serializers.JSONField(required=False)
    until_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = PointBank
        fields = ("id", "until_at", "info", "updated_at", "created_at", "point", "user", "margin",)
        expandable_fields = {
            "user": (PingoUserSerializer, {"many": False}),
            "margin": (MarginSerializer, {"many": False})
        }
