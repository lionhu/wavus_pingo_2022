from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rolepermissions.checkers import has_role
from django.db.models import F
from core.mixins import RedisMixin
from pingo.permissions import StaffActionPermission, SAFEActionPermission
from store.models import Category, Faq, Section, Logistic, Supplier, AddressBook
from store.serializers import CategorySerializer, FaqSerializer, SectionSerializer, LogisticSerializer, \
    SupplierSerializer, AddressBookSerializer
from store.mixins import DynamicQuerySetMixin
from store.permissions import AddressBookPermission
from pingo.conf import settings as pingo_settings
from django.contrib.auth import get_user_model
from core.functions import PrintExceptionError

import logging

logger = logging.getLogger("error_logger")
User = get_user_model()


__all__ = [
    "CategoryViewSet",
    "SectionViewSet",
    "FaqViewSet",
    "LogisticViewSet",
    "SupplierViewSet",
    "AddressBookViewSet",
]

class CategoryViewSet(DynamicQuerySetMixin, ModelViewSet):
    serializer_class = CategorySerializer
    model_class = Category
    dynamic_queryset = True
    permission_classes = (SAFEActionPermission,)
    filters = {}


class SectionViewSet(DynamicQuerySetMixin, RedisMixin, ModelViewSet):
    serializer_class = SectionSerializer
    model_class = Section
    dynamic_queryset = True
    sorted_by = ("index",)
    filters = {}
    # filters = {"is_valid": True}
    permission_classes = (SAFEActionPermission,)

    def list(self, request, *args, **kwargs):
        logger.error(self.__class__.__name__)
        cached_data = self.get_redis_data("sections", request)

        if pingo_settings.USE_REDIS_CACHE:
            if cached_data is None:
                response = super(self.__class__, self).list(request, *args, **kwargs)
                cached_data = response.data
                self.set_redis_data("sections", request, cached_data, 300)
        else:
            response = super(self.__class__, self).list(request, *args, **kwargs)
            cached_data = response.data

        return Response(cached_data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None, *args, **kwargs):
        cached_data = self.get_redis_data(f"section_{pk}", request)

        if pingo_settings.USE_REDIS_CACHE:
            if cached_data is None:
                response = super(self.__class__, self).retrieve(request, pk=None, *args, **kwargs)
                cached_data = response.data
                self.set_redis_data(f"section_{pk}", request, cached_data, 300)
        else:
            response = super(self.__class__, self).retrieve(request, pk=None, *args, **kwargs)
            cached_data = response.data

        return Response(cached_data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        self.remove_pattern_redis_cache("sections")
        return super(SectionViewSet, self).create(request, *args, **kwargs)

    def destroy(self, request, pk=None, *args, **kwargs):
        self.remove_pattern_redis_cache("sections")
        return super(SectionViewSet, self).destroy(request, pk, *args, **kwargs)


class FaqViewSet(DynamicQuerySetMixin, RedisMixin, ModelViewSet):
    serializer_class = FaqSerializer
    model_class = Faq
    dynamic_queryset = True
    sorted_by = ("index",)
    filters = {"is_valid": True}
    permission_classes = (StaffActionPermission,)

    def create(self, request, *args, **kwargs):
        logger.error(request.data)
        self.remove_pattern_redis_cache("sections")
        return super(FaqViewSet, self).create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        cached_data = self.get_redis_data("faqs", request)

        if pingo_settings.USE_REDIS_CACHE:
            if cached_data is None:
                response = super(self.__class__, self).list(request, *args, **kwargs)
                cached_data = response.data
                self.set_redis_data("faqs", request, cached_data, 300)
        else:
            response = super(self.__class__, self).list(request, *args, **kwargs)
            cached_data = response.data

        return Response(cached_data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None, *args, **kwargs):
        cached_data = self.get_redis_data(f"faq_{pk}", request)

        if pingo_settings.USE_REDIS_CACHE:
            if cached_data is None:
                response = super(self.__class__, self).retrieve(request, pk=None, *args, **kwargs)
                cached_data = response.data
                self.set_redis_data(f"faq_{pk}", request, cached_data, 300)
        else:
            response = super(self.__class__, self).retrieve(request, pk=None, *args, **kwargs)
            cached_data = response.data

        return Response(cached_data, status=status.HTTP_200_OK)

    def update(self, request, pk=None, *args, **kwargs):
        self.filters = {}
        self.remove_pattern_redis_cache("sections")
        return super(FaqViewSet, self).update(request, pk, *args, **kwargs)

    def destroy(self, request, pk=None, *args, **kwargs):
        self.filters = {}
        self.remove_pattern_redis_cache("sections")
        return super(FaqViewSet, self).destroy(request, pk, *args, **kwargs)


class LogisticViewSet(DynamicQuerySetMixin, ModelViewSet):
    serializer_class = LogisticSerializer
    model_class = Logistic
    dynamic_queryset = True
    permission_classes = (SAFEActionPermission,)
    filters = {}


class SupplierViewSet(DynamicQuerySetMixin, ModelViewSet):
    serializer_class = SupplierSerializer
    permission_classes = (IsAuthenticated,)
    model_class = Supplier
    dynamic_queryset = True
    filters = {}
    sorted_by = ("-id",)

    @action(methods=["post"], detail=False)
    def retrieve_by_email(self, request, *args, **kwargs):
        try:
            email = request.data.get("email", None)
            supplier = Supplier.objects.filter(user__email=email).first()
            serializer = self.get_serializer(supplier, many=False)
            return Response({
                "supplier": serializer.data,
            }, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({
                "message": PrintExceptionError(err)
            }, status=status.HTTP_400_BAD_REQUEST)


class AddressBookViewSet(ModelViewSet):
    serializer_class = AddressBookSerializer
    permission_classes = (AddressBookPermission,)
    filters = {}

    def get_queryset(self):
        if has_role(self.request.user, ["client", "member"]):
            return AddressBook.objects.filter(user=self.request.user)
        else:
            return AddressBook.objects.all()

    def create(self, request, *args, **kwargs):
        request.data["user"] = request.user.id
        return super(AddressBookViewSet, self).create(request, *args, **kwargs)

