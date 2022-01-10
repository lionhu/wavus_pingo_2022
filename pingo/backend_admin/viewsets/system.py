from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache
from pingo.conf import settings as pingo_settings
from core.mixins import RedisMixin
from rest_framework.permissions import IsAuthenticated
from store.models import Category, Item, Supplier, Logistic
from store.serializers import CategorySerializer, ItemSerializer, ItemFullSerializer, SupplierSerializer, \
    LogisticSerializer
from django.contrib.auth import get_user_model
from core.functions import PrintExceptionError
from store.tasks import rebuild_elasticsearch_indexing
import logging

logger = logging.getLogger("error_logger")
User = get_user_model()

__all__ = [
    "SystemViewSet",
]


class SystemViewSet(GenericViewSet, RedisMixin):
    permission_classes = (IsAuthenticated,)

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

    @action(detail=False, methods=["post"])
    def reset_redis(self, request, pk=None):
        try:
            cache.clear()
            rebuild_elasticsearch_indexing.delay()

            return Response({
                'result': True,
            }, status=status.HTTP_200_OK)

        except Exception as error:
            return Response({
                'error_message":"': PrintExceptionError(error)
            }, status=status.HTTP_400_BAD_REQUEST)
