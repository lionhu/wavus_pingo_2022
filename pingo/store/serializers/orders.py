from rest_framework import serializers
from rest_flex_fields import FlexFieldsModelSerializer
from store.models import Variation, OrderItem, Order
from djoser.serializers import UserSerializer
from rolepermissions.checkers import has_role
from store.models import OrderItem, Variation
from store.serializers import ContextFlexFieldsModelSerialier, LogisticSerializer, VariationSerializer, VariationFullSerializer, ItemFullSerializer
from authentication.serializers import PingoUserSerializer
import logging

logger = logging.getLogger("error_logger")

__all__ = [
    "OrderItemFULLSerializer",
    "OrderSerializer",
    "OrderItemSerializer",
]


class OrderItemFULLSerializer(ContextFlexFieldsModelSerialier):
    variation = serializers.SerializerMethodField("get_variation_serializer")

    class Meta:
        model = OrderItem
        fields = ("id", "order", "ordered", "variation", "quantity",
                  "final_price", "status",  "total_price", "total_purchase_price", "profit",
                  )
        private_fields = ("total_purchase_price", "profit",)

    def get_variation_serializer(self,obj):
        serializer_context = {'request': self.context.get('request')}
        variation = Variation.objects.get(pk=obj.variation_id)
        serializer = VariationSerializer(
            variation, many=False, context=serializer_context)
        return serializer.data
    
class OrderSerializer(ContextFlexFieldsModelSerialier):
    order_items = serializers.SerializerMethodField(
        "get_order_items_serializer")
    point_usage = serializers.JSONField()
    order_bonus = serializers.JSONField()
    # cart_items = serializers.JSONField()
    json_shippingaddress = serializers.JSONField()
    delivery_info = serializers.JSONField(required=False)
    chargeAmount = serializers.IntegerField()
    Total = serializers.IntegerField()
    Qty = serializers.IntegerField()

    class Meta:
        model = Order
        fields = ('id',  'slug', "type", "status", "supplier_paid", 'start_date', 'ordered_at', "ordered",
                  "is_valid",  "json_shippingaddress", "Qty", "Total", "chargeAmount", "point_usage", "order_bonus",
                  "message", "is_paid", "payment_status", "payment_method", "payment_id", "payment_info",
                  "is_delivered", "delivered_at", "delivery_info", 
                  "user", "logistic", "order_items",)
        read_only_fields = ("payment_status", "payment_method", "payment_id", "payment_info", 'slug',
                            "orderitems", 'start_date', 'ordered_at', "ordered",
                            "is_valid", "is_paid", "json_shippingaddress", "supplier_paid",)
        expandable_fields = {
            "user": (PingoUserSerializer, {"many": False}),
            "logistic": (LogisticSerializer, {"many": False}),
            # "orderitems": (OrderItemFULLSerializer, {"many": True, "required": False}),
        }
        private_fields = ("payment_method", "payment_id", "payment_info",)

    def get_order_items_serializer(self, obj):
        serializer_context = {'request': self.context.get('request')}
        items = OrderItem.objects.all().filter(order=obj)
        serializer = OrderItemFULLSerializer(
            items, many=True, context=serializer_context)
        return serializer.data
    
    def create(self, validated_data):
        order = Order.objects.create(**validated_data)
        if len(validated_data["cart_items"]):
            for item in validated_data["cart_items"]:
                variation = Variation.objects.get(pk=item["variant"]["id"])
                OrderItem.objects.create(
                    item_id=item["product"]["id"],
                    user=order.user,
                    order=order,
                    variation=variation,
                    quantity=item["quantity"],
                    final_price=variation.price
                )
        return order


class OrderItemSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = OrderItem
        fields = ("id", "ordered", "quantity", "final_price", "status",
                  "total_price", "profit",
                  "order", "user", "variation", "item",
                  )
        expandable_fields = {
            "variation": (VariationFullSerializer, {"many": False}),
            "order": (OrderSerializer, {"many": False}),

            "item": (ItemFullSerializer, {"many": False}),
            "user": (UserSerializer, {"many": False}),  # 多対多
        }
        private_fields = ("total_purchase_price",)

    def __init__(self, *args, **kwargs):
        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)
        request = self.context.get('request', None)
        print("OrderItemSerializer __init___")
        print(request)
        if request is not None and  has_role(request.user, ["superadmin", "staff", "supplier"]):
            if hasattr(self.Meta, "private_fields") and len(self.Meta.private_fields) > 0:

                print("OrderItemSerializer push private_fields")
                for field_name in self.Meta.private_fields:
                    self.fields.push(field_name)
