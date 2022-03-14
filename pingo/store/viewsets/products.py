from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rolepermissions.checkers import has_role
from django.core.cache import cache
from django.db.models import F
from core.mixins import RedisMixin
from pingo.permissions import StaffActionPermission, SAFEActionPermission
from store.models import Item, Variation, ItemSliderImage, ViewProductHistory, Comment, Thumbs, Favorite, InventoryHistory
from store.serializers import ItemSerializer, VariationSerializer, \
    ItemSliderImageSerializer, ViewProductHistorySerializer, CommentSerializer, ThumbsSerializer, \
    FavoriteSerializer, InventorySerializer,  CommentFullSerializer
from store.mixins import DynamicQuerySetMixin
from store.permissions import  CommentPermission, ProductPermission, ItemSliderImagePermission, VariationImagePermission
from pingo.conf import settings as pingo_settings
from store.tasks import recore_viewproduct_event
from core.functions import PrintExceptionError, generate_user_product_qr
from django.contrib.auth import get_user_model

import logging

logger = logging.getLogger("error_logger")
User = get_user_model()


__all__ = [
    "ProductViewSet",
    "VariationViewSet",
    "ItemSliderImageViewSet",
    "ViewProductHistoryViewSet",
    "CommentViewSet",
    "ThumbsViewSet",
    "FavoriteViewSet",
    "InventoryViewSet",
]


class ProductViewSet(DynamicQuerySetMixin, RedisMixin, ModelViewSet):
    serializer_class = ItemSerializer
    model_class = Item
    dynamic_queryset = True
    permission_classes = (ProductPermission,)
    filters = {
        "is_valid": True
    }
    sorted_by = ("-created_at",)

    def create(self, request, *args, **kwargs):
        self.filters = {}
        response = super(self.__class__, self).create(request, *args, **kwargs)
        category_id = response.data["category"]

        category_product_keys = pingo_settings.REDIS_KEYS["CATEGORY_PRODUCTS"].format(category_id)
        self.remove_pattern_redis_cache(category_product_keys)
        return response

    def destroy(self, request, pk=None, *args, **kwargs):
        self.filters = {}
        item = Item.objects.get(pk=pk)

        product_keys = pingo_settings.REDIS_KEYS["PRODUCT"].format(pk)
        self.remove_pattern_redis_cache(product_keys)

        category_product_keys = pingo_settings.REDIS_KEYS["CATEGORY_PRODUCTS"].format(item.category.id)
        self.remove_pattern_redis_cache(category_product_keys)

        return super(self.__class__, self).destroy(request, pk, *args, **kwargs)

    def retrieve(self, request, pk=None, *args, **kwargs):
        print(request.user)
        if not request.user.is_anonymous:
            recore_viewproduct_event.delay(user_id=request.user.id, item_id=pk, type="REGULAR")

        if has_role(request.user, ["superadmin", "staff", "supplier"]):
            self.filters = {}


        response = super(self.__class__, self).retrieve(request, pk, *args, **kwargs)
        product_data = response.data

        return Response({"item": product_data}, status=status.HTTP_200_OK)
    
    
        prefix_redis = f"regular_product_{pk}"
        product_data = self.get_redis_data(prefix_redis, request)

        if pingo_settings.USE_REDIS_CACHE:
            if product_data is None:
                response = super(self.__class__, self).retrieve(request, pk, *args, **kwargs)
                product_data = response.data
                self.set_redis_data(prefix_redis, request, product_data, 300)
        else:
            response = super(self.__class__, self).retrieve(request, pk, *args, **kwargs)
            product_data = response.data

        return Response({"item": product_data}, status=status.HTTP_200_OK)

    def update(self, request, pk=None, *args, **kwargs):
        self.filters = {}
        # in case item category information changed, two related category product keys will update
        item = Item.objects.get(pk=pk)

        product_keys = pingo_settings.REDIS_KEYS["PRODUCT"].format(pk)
        self.remove_pattern_redis_cache(product_keys)

        category_product_keys = pingo_settings.REDIS_KEYS["CATEGORY_PRODUCTS"].format(item.category.id)
        self.remove_pattern_redis_cache(category_product_keys)

        logger.error(request.data)
        response = super(self.__class__, self).update(request, pk, *args, **kwargs)

        category_product_keys = pingo_settings.REDIS_KEYS["CATEGORY_PRODUCTS"].format(response.data["category"])
        self.remove_pattern_redis_cache(category_product_keys)

        return super(self.__class__, self).retrieve(request, pk, *args, **kwargs)

    @action(detail=True, methods=["post"])
    def update_post_image(self, request, pk=None, *args, **kwargs):
        self.filters = {}
        item = Item.objects.get(pk=pk)
        image = request.data.get("image", None)
        if image is not None:
            item.image = image
            item.save()

            serializer = self.get_serializer(item, many=False)

            product_keys = pingo_settings.REDIS_KEYS["PRODUCT"].format(pk)
            self.remove_pattern_redis_cache(product_keys)

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["get"])
    def get_introduce_qr(self, request, pk=None):
        try:
            share_code = pingo_settings.REDIS_KEYS["USER_PRODUCT_SHARE_QRCODE"].format(request.user.id, pk)
            share_code_data = cache.get(share_code)
            if share_code_data is None:
                product = Item.objects.get(pk=pk)
                share_code_data = generate_user_product_qr(request.user, product, "sharebuy")
                cache.set(share_code, share_code_data, 1200)

            return Response(share_code_data, status=status.HTTP_200_OK)

        except Exception as err:
            return Response({
                "error": "SUPERADMIN_PRODUCT_GET_ERR01",
                'message":"': 'Failed to get introduce picture from backend',
                'error_message":"': PrintExceptionError(err)
            }, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        try:
            self.filters.update({"type": "REGULAR"})
            if has_role(request.user, ["superadmin", "staff", "supplier"]):
                self.filters = {}

            logger.error(self.filters)
            prefix_redis = "category_products"

            if pingo_settings.USE_REDIS_CACHE:
                category_products_data = self.get_redis_data(prefix_redis, request)
                if category_products_data is None:
                    response = super(self.__class__, self).list(request, *args, **kwargs)
                    category_products_data = response.data
                    self.set_redis_data(prefix_redis, request, category_products_data, 300)
            else:
                response = super(self.__class__, self).list(request, *args, **kwargs)
                category_products_data = response.data

            return Response(category_products_data, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({
                "message": PrintExceptionError(err)
            }, status=status.HTTP_400_BAD_REQUEST)


class VariationViewSet(DynamicQuerySetMixin, RedisMixin, ModelViewSet):
    serializer_class = VariationSerializer
    permission_classes = (VariationImagePermission,)
    model_class = Variation
    dynamic_queryset = True
    filters = {}
    private_fields = "purchase_price"

    @action(detail=True, methods=["post"])
    def update_image(self, request, pk=None, *args, **kwargs):
        variation = Variation.objects.get(pk=pk)
        image = request.data.get("image", None)
        if image is not None:
            variation.image = image
            variation.save()

            category_product_keys = pingo_settings.REDIS_KEYS["CATEGORY_PRODUCTS"].format(variation.item.id)
            self.remove_pattern_redis_cache(category_product_keys)

            return super(self.__class__, self).retrieve(request, pk, *args, **kwargs)
        return Response({}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None, *args, **kwargs):
        variation = Variation.objects.get(pk=pk)
        category_product_keys = pingo_settings.REDIS_KEYS["CATEGORY_PRODUCTS"].format(variation.item.id)
        self.remove_pattern_redis_cache(category_product_keys)
        return super(VariationViewSet, self).destroy(request, pk, *args, **kwargs)

    def update(self, request, pk=None, *args, **kwargs):
        variation = Variation.objects.get(pk=pk)
        category_product_keys = pingo_settings.REDIS_KEYS["CATEGORY_PRODUCTS"].format(variation.item.id)
        self.remove_pattern_redis_cache(category_product_keys)
        return super(VariationViewSet, self).update(request, pk, *args, **kwargs)


class ItemSliderImageViewSet(DynamicQuerySetMixin, RedisMixin, ModelViewSet):
    serializer_class = ItemSliderImageSerializer
    permission_classes = (ItemSliderImagePermission,)
    model_class = ItemSliderImage
    dynamic_queryset = True
    filters = {}

    def create(self, request, *args, **kwargs):
        pk = request.data.get("item", None)
        product_keys = pingo_settings.REDIS_KEYS["PRODUCT"].format(pk)
        self.remove_pattern_redis_cache(product_keys)

        return super(ItemSliderImageViewSet, self).create(request, *args, **kwargs)


class ViewProductHistoryViewSet(DynamicQuerySetMixin, RedisMixin, ModelViewSet):
    serializer_class = ViewProductHistorySerializer
    permission_classes = (SAFEActionPermission,)
    model_class = ViewProductHistory
    dynamic_queryset = True
    filters = {}

    def list(self, request, *args, **kwargs):
        prefix_redis = pingo_settings.REDIS_KEYS["VIEW_HISTORIES"].format(request.user.id)
        cached_data = self.get_redis_data(prefix_redis, request)

        if pingo_settings.USE_REDIS_CACHE:
            if cached_data is None:
                self.filters = {
                    "user": request.user.id
                }
                response = super(ViewProductHistoryViewSet, self).list(request, *args, **kwargs)
                cached_data = response.data
                self.set_redis_data(prefix_redis, request, cached_data, 300)
        else:
            response = super(ViewProductHistoryViewSet, self).list(request, *args, **kwargs)
            cached_data = response.data

        return Response(cached_data, status=status.HTTP_200_OK)

    @action(methods=["get"], detail=True)
    def user_list(self, request, pk=None, *args, **kwargs):
        viewhistories = ViewProductHistory.objects.filter(user__id=pk)
        serializer = self.get_serializer(viewhistories, many=True)
        cached_data = serializer.data
        return Response(cached_data, status=status.HTTP_200_OK)


class CommentViewSet(DynamicQuerySetMixin, RedisMixin, ModelViewSet):
    serializer_class = CommentSerializer
    model_class = Comment
    dynamic_queryset = True
    filters = {}
    sorted_by = ("-created_at",)
    permission_classes = (CommentPermission,)

    def list(self, request, *args, **kwargs):
        item_id = request.query_params.get("item", None)
        self.filters.update({
            "item": item_id,
            "item_type": "REGULAR",
        })
        prefix_redis = f"product_{item_id}_comments"
        cached_data = self.get_redis_data(prefix_redis, request)

        if pingo_settings.USE_REDIS_CACHE:
            if cached_data is None:
                response = super(CommentViewSet, self).list(request, *args, **kwargs)
                cached_data = response.data
                self.set_redis_data(prefix_redis, request, cached_data, 300)
        else:
            response = super(CommentViewSet, self).list(request, *args, **kwargs)
            cached_data = response.data

        return Response(cached_data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        request.data["user"] = request.user.id
        request.data["item_type"] = "REGULAR"
        response = super(CommentViewSet, self).create(request, *args, **kwargs)
        new_comment = Comment.objects.get(pk=response.data["id"])
        serializer = CommentFullSerializer(new_comment, many=False)

        if pingo_settings.SEND_SUPERADMIN_COMMENT_CREATED_EMAIL:
            context = {
                "subject": "商品コメント",
                "type": "Comment",
                "content": "新しい商品コメントが入りました。ご確認ください。",
                "item_name": new_comment.item.item_name,
                "username": request.user.username,
                "comment": new_comment.content,
                "button_blue_text": f"承認",
                "button_blue_url": f"https://www.pingo.jp/backend/operations?type=comment&approved=true&comment_id={new_comment.id}",
                "button_grey_text": f"却下",
                "button_grey_url": f"https://www.pingo.jp/backend/operations?type=comment&approved=false&comment_id={new_comment.id}",
            }
            pingo_settings.EMAIL.new_comment_notification(request, context=context).send([pingo_settings.ADMIN_EMAIL])

        return Response({
            "comment": serializer.data
        }, status=status.HTTP_200_OK)

    @action(methods=["get"], detail=False)
    def list_pingo(self, request, *args, **kwargs):
        item_id = request.query_params.get("item", None)
        self.filters.update({
            "item": item_id,
            "item_type": "PINGO",
        })
        prefix_redis = f"pingo_product_{item_id}_comments"
        cached_data = self.get_redis_data(prefix_redis, request)

        if pingo_settings.USE_REDIS_CACHE:
            if cached_data is None:
                response = super(CommentViewSet, self).list(request, *args, **kwargs)
                cached_data = response.data
                self.set_redis_data(prefix_redis, request, cached_data, 300)
        else:
            response = super(CommentViewSet, self).list(request, *args, **kwargs)
            cached_data = response.data

        return Response(cached_data, status=status.HTTP_200_OK)

    @action(methods=["post"], detail=False)
    def create_pingo(self, request, *args, **kwargs):
        request.data["user"] = request.user.id
        request.data["item_type"] = "PINGO"
        response = super(CommentViewSet, self).create(request, *args, **kwargs)
        new_comment = Comment.objects.get(pk=response.data["id"])
        serializer = CommentFullSerializer(new_comment, many=False)

        item_id = request.data.get("item", None)
        prefix_redis = f"pingo_product_{item_id}_comments"
        self.remove_pattern_redis_cache(prefix_redis)

        return Response({
            "comment": serializer.data
        }, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None, *args, **kwargs):
        logger.error(f"update comments: pk= {pk}")
        # self.filters = {}
        comment = Comment.objects.get(pk=pk, user=request.user)

        prefix_redis = f"product_{comment.item.id}_comments"
        self.remove_pattern_redis_cache(prefix_redis)

        return super(CommentViewSet, self).destroy(request, pk, *args, **kwargs)

    def update(self, request, pk=None, *args, **kwargs):
        response = super(CommentViewSet, self).update(request, pk, *args, **kwargs)
        return response

    @action(methods=["get"], detail=True)
    def approve(self, request, pk=None, *args, **kwargs):
        try:
            approved = self.request.query_params.get("query", None)
            comment = Comment.objects.get(pk=pk)
            print(approved)
            if approved == "true":
                comment.checked = True
                comment.approved = True
            else:
                comment.checked = True
                comment.approved = False
            comment.save()
            return Response({
                "message": "approve comment",
                "comment_id": comment.id,
                "approved": comment.approved,
            }, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({
                "message": PrintExceptionError(err)
            }, status=status.HTTP_400_BAD_REQUEST)


class ThumbsViewSet(DynamicQuerySetMixin, ModelViewSet):
    serializer_class = ThumbsSerializer
    model_class = Thumbs
    dynamic_queryset = True
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        comment = request.data.get("comment", None)
        thumb_type = request.data.get("thumb_type", None)

        thumb = Thumbs.objects.filter(comment_id=comment, user=request.user, thumb_type=thumb_type).first()

        if thumb is not None:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

        request.data["user"] = request.user.id
        response = super(ThumbsViewSet, self).create(request, *args, **kwargs)
        if thumb_type == "up" and int(comment):
            Comment.objects.filter(pk=comment).update(thumbs_up=F("thumbs_up") + 1)
        else:
            Comment.objects.filter(pk=comment).update(thumbs_down=F("thumbs_down") + 1)

        return response


class FavoriteViewSet(DynamicQuerySetMixin, RedisMixin, ModelViewSet):
    serializer_class = FavoriteSerializer
    permission_classes = (IsAuthenticated,)
    model_class = Favorite
    dynamic_queryset = True
    filters = {}
    sorted_by = ("-created_at",)

    def list(self, request, *args, **kwargs):
        prefix_redis = pingo_settings.REDIS_KEYS["MY_FAVORITES"].format(
            request.user.id)
        cached_data = self.get_redis_data(prefix_redis, request)

        if pingo_settings.USE_REDIS_CACHE:
            if cached_data is None:
                self.filters = {
                    "user": request.user.id
                }
                response = super(self.__class__, self).list(
                    request, *args, **kwargs)
                cached_data = response.data
                self.set_redis_data(prefix_redis, request, cached_data, 300)
        else:
            response = super(self.__class__, self).list(
                request, *args, **kwargs)
            cached_data = response.data

        return Response(cached_data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        try:
            prefix_redis = pingo_settings.REDIS_KEYS["MY_FAVORITES"].format(
                request.user.id)

            item_id = request.data.get("item", None)
            favorite = Favorite.objects.filter(
                item__id=item_id, user=request.user).first()
            if favorite is None:
                request.data["user"] = request.user.id
                response_obj = super(self.__class__, self).create(
                    request, *args, **kwargs)

                self.remove_pattern_redis_cache(prefix_redis)

                return response_obj
            return Response({
                "message": "wishlist.existed",
            }, status=status.HTTP_409_CONFLICT)
        except Exception as err:
            return Response({
                "message": PrintExceptionError(err)
            }, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None, *args, **kwargs):
        prefix_redis = pingo_settings.REDIS_KEYS["MY_FAVORITES"].format(
            request.user.id)
        self.filters = {
            "user": request.user.id
        }
        self.remove_pattern_redis_cache(prefix_redis)
        return super(self.__class__, self).destroy(request, pk=None, *args, **kwargs)


class InventoryViewSet(DynamicQuerySetMixin, ModelViewSet):
    serializer_class = InventorySerializer
    model_class = InventoryHistory
    dynamic_queryset = True
    filters = {}
    private_fields = "info,id"
    sorted_by = ("-id",)
    permission_classes = (StaffActionPermission,)

