from rest_framework import serializers
from rest_flex_fields import FlexFieldsModelSerializer
from store.models import PointBank, Margin
from authentication.serializers import PingoUserSerializer
import logging

logger = logging.getLogger("error_logger")

__all__ = [
    "MarginSerializer",
    "PointBankSerializer",
]


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
        fields = ("id", "until_at", "info", "updated_at",
                  "created_at", "point", "user", "margin",)
        expandable_fields = {
            "user": (PingoUserSerializer, {"many": False}),
            "margin": (MarginSerializer, {"many": False})
        }
