from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from pingo.conf import settings as pingo_settings
from core.mixins import RedisMixin
from pingo.permissions import StaffActionPermission, SAFEActionPermission
from store.models import Category, Item, Supplier, Logistic
from store.serializers import CategorySerializer, ItemSerializer, ItemFullSerializer, SupplierSerializer, LogisticSerializer
from django.contrib.auth import get_user_model

import logging

logger = logging.getLogger("error_logger")
User = get_user_model()


class SystemViewSet(GenericViewSet, RedisMixin):

    @action(detail=False, methods=["post"])
    def store_system_info(self, request, *args, **kwargs):
        prefix_redis = pingo_settings.REDIS_KEYS["CATEGORIES"]
        categories_data = self.get_redis_data(prefix_redis, request)

        if pingo_settings.USE_REDIS_CACHE:
            if categories_data is None:
                categories = Category.objects.filter(title=pingo_settings.SHOP_SETTINGS["ROOT_SHOP_MENU"]).first()
                serializer_categories = CategorySerializer(categories, many=False)
                categories_data = serializer_categories.data
                self.set_redis_data(prefix_redis, request, categories_data, 300)
        else:
            categories = Category.objects.filter(title=pingo_settings.SHOP_SETTINGS["ROOT_SHOP_MENU"]).first()
            serializer_categories = CategorySerializer(categories, many=False)
            categories_data = serializer_categories.data

        return Response({
            "result": True,
            "message": "system information of nichiei store",
            "categories": categories_data,
        }, status=status.HTTP_200_OK)


class AdminSystemViewSet(GenericViewSet, RedisMixin):
    permission_classes = (StaffActionPermission,)

    @action(detail=False, methods=["get"])
    def backend_system_info(self, request, *args, **kwargs):
        suppliers = Supplier.objects.all()
        serializer_suppliers = SupplierSerializer(instance=suppliers, many=True)

        categories = Category.objects.filter(title=pingo_settings.SYSTEM["ROOT_MENU"]).first()
        serializer_categories = CategorySerializer(categories, many=False)

        logistics = Logistic.objects.all()
        serializer_logistics = LogisticSerializer(logistics, many=True)

        return Response({
            "menuitems": serializer_categories.data,
            "suppliers": serializer_suppliers.data,
            "logistics": serializer_logistics.data,
        }, status=status.HTTP_200_OK)
