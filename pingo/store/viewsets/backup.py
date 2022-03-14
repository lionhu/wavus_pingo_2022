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
from store.models import Category, Faq, Section, Logistic, Supplier, AddressBook, Item, \
    Variation, ItemSliderImage, ViewProductHistory, Comment, Thumbs, Favorite, \
    OrderItem, InventoryHistory, Order, Margin, PointBank
from store.serializers import CategorySerializer, FaqSerializer, SectionSerializer, LogisticSerializer, \
    SupplierSerializer, AddressBookSerializer, ItemSerializer, VariationSerializer, \
    ItemSliderImageSerializer, ViewProductHistorySerializer, CommentSerializer, ThumbsSerializer, \
    FavoriteSerializer, OrderItemSerializer, InventorySerializer, OrderSerializer, PointBankSerializer, \
    MarginSerializer, CommentFullSerializer, ItemElasticSearchSerializer
from store.mixins import DynamicQuerySetMixin, OrderMixin, OrderPointDistribution, \
    PointBankMixin, SquarePaymentMixin
from store.permissions import AddressBookPermission, CommentPermission, PointBankPermission, MarginPermission, \
    SupplierPermission, ProductPermission, ItemSliderImagePermission, VariationImagePermission
from pingo.conf import settings as pingo_settings
from pingo.exceptions import NoAccessPermission
from store.tasks import recore_viewproduct_event
from store.signals import signalOrderItemStatusChanged, signalOrderItemSupplierPaymentChanged
from store.exceptions import GenerateOrderError_InsufficientPoint, GenerateOrderError_CreditCardFailed
from core.functions import PrintExceptionError, generate_user_product_qr, extract_query_param_filter
from django.contrib.auth import get_user_model

import logging

logger = logging.getLogger("error_logger")
User = get_user_model()


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


class FavoriteViewSet(DynamicQuerySetMixin, RedisMixin, ModelViewSet):
    serializer_class = FavoriteSerializer
    permission_classes = (IsAuthenticated,)
    model_class = Favorite
    dynamic_queryset = True
    filters = {}
    sorted_by = ("-created_at",)

    def list(self, request, *args, **kwargs):
        prefix_redis = pingo_settings.REDIS_KEYS["MY_FAVORITES"].format(request.user.id)
        cached_data = self.get_redis_data(prefix_redis, request)

        if pingo_settings.USE_REDIS_CACHE:
            if cached_data is None:
                self.filters = {
                    "user": request.user.id
                }
                response = super(self.__class__, self).list(request, *args, **kwargs)
                cached_data = response.data
                self.set_redis_data(prefix_redis, request, cached_data, 300)
        else:
            response = super(self.__class__, self).list(request, *args, **kwargs)
            cached_data = response.data

        return Response(cached_data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        try:
            prefix_redis = pingo_settings.REDIS_KEYS["MY_FAVORITES"].format(request.user.id)

            item_id = request.data.get("item", None)
            favorite = Favorite.objects.filter(item__id=item_id, user=request.user).first()
            if favorite is None:
                request.data["user"] = request.user.id
                response_obj = super(self.__class__, self).create(request, *args, **kwargs)

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
        prefix_redis = pingo_settings.REDIS_KEYS["MY_FAVORITES"].format(request.user.id)
        self.filters = {
            "user": request.user.id
        }
        self.remove_pattern_redis_cache(prefix_redis)
        return super(self.__class__, self).destroy(request, pk=None, *args, **kwargs)


class ProductViewSet(DynamicQuerySetMixin, RedisMixin, ModelViewSet):
    serializer_class = ItemSerializer
    model_class = Item
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


# class SearchProducts(PaginatedElasticSearchAPIView):
#     serializer_class = ItemElasticSearchSerializer
#     document_class = ProductDocument
#
#     def generate_q_expression(self, query):
#         return Q_elasticsearch(
#             'multi_match', query=query,
#             fields=[
#                 'item_name',
#                 'description',
#             ], fuzziness='auto')
#
#
# class FilterProductsViewSet(ElasticSearchViewSet):
#     serializer_class = ItemElasticSearchSerializer
#     document_class = ProductDocument
#     generate_q_expression = None
#
#     @action(methods=["get"], detail=False)
#     def valid(self, request, *args, **kwargs):
#         self.generate_q_expression = Q_elasticsearch('match', is_valid=True)
#         return super(FilterProductsViewSet, self).search(request, *args, **kwargs)
#
#     @action(methods=["get"], detail=False)
#     def ofLabel(self, request, *args, **kwargs):
#         query = self.request.query_params.get("query", None)
#         # self.generate_q_expression = Q_elasticsearch('match', labels=query)
#         self.generate_q_expression = Q_elasticsearch(
#             'bool',
#             must=[
#                 Q_elasticsearch('match', labels=query),
#                 Q_elasticsearch('match', is_valid=True)
#             ])
#         return super(FilterProductsViewSet, self).search(request, *args, **kwargs)
#
#     @action(methods=["get"], detail=False)
#     def ofCategory(self, request, *args, **kwargs):
#         query = self.request.query_params.get("query", None)
#         self.generate_q_expression = Q_elasticsearch(
#             'bool',
#             must=[
#                 Q_elasticsearch('match', category_to_string=query),
#                 Q_elasticsearch('match', is_valid=True)
#             ])
#         return super(FilterProductsViewSet, self).search(request, *args, **kwargs)
#
#     @action(methods=["get"], detail=False)
#     def by_name_description(self, request, *args, **kwargs):
#         query = self.request.query_params.get("query", None)
#         self.generate_q_expression = Q_elasticsearch(
#             'multi_match', query=query,
#             fields=[
#                 'item_name',
#                 'description',
#             ], fuzziness='auto')
#
#         return super(FilterProductsViewSet, self).search(request, *args, **kwargs)
#
#
# class SearchProductsOfCategory(PaginatedElasticSearchAPIView):
#     serializer_class = ItemElasticSearchSerializer
#     document_class = ProductDocument
#
#     def generate_q_expression(self, query):
#         return Q_elasticsearch(
#             'multi_match', query=query,
#             fields=[
#                 'category.title',
#             ], fuzziness='auto')


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


class OrderViewSet(DynamicQuerySetMixin,
                   OrderMixin,
                   PointBankMixin,
                   SquarePaymentMixin,
                   ModelViewSet):
    serializer_class = OrderSerializer
    model_class = Order
    dynamic_queryset = True
    filters = {}
    private_fields = ""
    sorted_by = ("-ordered_at",)
    permission_classes = (IsAuthenticated,)

    @action(methods=["get"], detail=False)
    def me(self, request, *args, **kwargs):
        self.filters = {
            "type": "REGULAR",
            "user": request.user
        }
        return super(OrderViewSet, self).list(request, *args, **kwargs)

    @action(methods=["post"], detail=False)
    def check_inventory(self, request, *args, **kwargs):
        cart_items = request.data.get("cart_items", None)
        return Response(
            self.check_order_inventory(cart_items),
            status=status.HTTP_200_OK
        )

    def create(self, request, *args, **kwargs):
        order = None
        try:
            message = "Not access permission"
            if has_role(request.user, ["superadmin", "staff", "supplier"]):
                return Response({
                    "message": message
                }, status=status.HTTP_403_FORBIDDEN)

            request.data["user"] = request.user.id
            logger.error(request.data)
            self.check_order_data(request.data)

            point_usage = request.data.get("point_usage", None)
            cart_use_point = int(point_usage["use_point"])
            nonce = request.data.get("nonce", None)
            request.data.pop("nonce")

            order_serializer = self.get_serializer(data=request.data)
            if order_serializer.is_valid(raise_exception=True):
                logger.error("payment OK")
                order = order_serializer.save()

                # CreditCard Payment
                if order.Total == order.chargeAmount and nonce:
                    logger.error(" Pay by Creditcard")
                    pay_order_with_card = self.pay_order_byCreditCard("REGULAR", order, nonce)

                    order.payment_info = pay_order_with_card["payment_details"]
                    order.payment_method = "CARD"
                    order.payment_status = pay_order_with_card["payment_status"]
                    order.payment_id = pay_order_with_card["payment_id"]
                    order.is_paid = True
                    order.is_valid = True
                    order.save()

                    self.distribute_introduction_point(request.user, order)
                    self.distribute_self_join_point(request.user, order)

                    objPointsDistributor = OrderPointDistribution(order)
                    objPointsDistributor.distribute_order_points()
                # MIX Payment
                elif order.chargeAmount > 0 and order.Total > order.chargeAmount and nonce:
                    logger.error(" Pay by MIX")
                    holdPointInfo = self.pointbank_user_totalpoint(request.user.id)
                    if cart_use_point > holdPointInfo:
                        raise GenerateOrderError_InsufficientPoint

                    pay_order_with_card = self.pay_order_byCreditCard(order, nonce)

                    order.payment_info = pay_order_with_card["payment_details"]
                    order.payment_status = pay_order_with_card["payment_status"]
                    order.payment_method = "MIX"
                    order.payment_id = pay_order_with_card["payment_id"]
                    order.is_paid = True
                    order.is_valid = True
                    order.save()

                    self.pointbank_use_point(request.user.id, cart_use_point)

                    Margin.objects.create(
                        type="PURCHASE_ORDER",
                        order_type="REGULAR",
                        user=request.user,
                        fromuser=request.user,
                        amount=cart_use_point,
                        is_valid=True,
                        is_refound=-1,
                        from_orderID=order.id,
                        pointbank_saved=True,
                        info={"order_id": order.id}
                    )
                # Point Payment
                else:
                    # Pay by  Point
                    holdPointInfo = self.pointbank_user_totalpoint(request.user.id)
                    logger.error("user holdPointInfo:{}, want to user point:{}".format(holdPointInfo, cart_use_point))

                    if cart_use_point > holdPointInfo:
                        raise GenerateOrderError_InsufficientPoint

                    self.pointbank_use_point(request.user.id, cart_use_point)
                    Margin.objects.create(
                        type="PURCHASE_ORDER",
                        order_type="REGULAR",
                        user=request.user,
                        fromuser=request.user,
                        amount=cart_use_point,
                        is_valid=True,
                        is_refound=-1,
                        from_orderID=order.id,
                        pointbank_saved=True,
                        info={"order_id": order.id}
                    )
                    order.payment_method = "POINT"
                    order.payment_info = {
                        "method": "POINT",
                        "point_info": {"amount": cart_use_point}
                    }
                    order.ordered = True
                    order.is_paid = True
                    order.is_valid = True
                    order.save()

                logger.error("notify member new order")
                if pingo_settings.SEND_MEMBER_NEW_ORDER_EMAIL:
                    pingo_settings.TASKS.notify_member_new_order(order.id)

                logger.error("notify superadmin new order")
                if pingo_settings.SEND_SUPERADMIN_NEW_ORDER_EMAIL:
                    pingo_settings.TASKS.notify_superadmin_new_order(order.id)

                logger.error("notify supplier new order")
                if pingo_settings.SUPPLIER_AUTO_SEND_NEW_ORDERITEM_EMAIL:
                    _ids = [orderitem.id for orderitem in order.orderitems.all()]
                    if len(_ids):
                        pingo_settings.TASKS.notify_supplier_orderitem_batch(_ids)

                logger.error("notify user new order")

                return Response({
                    "message": "order data OK",
                    "order": order_serializer.data,
                    "pointbank_balance": self.pointbank_user_totalpoint(request.user.id)
                }, status=status.HTTP_200_OK)

            return Response({
                "message": "bad order request"
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:

            if order is not None:
                OrderItem.objects.filter(order=order).delete()
                Margin.objects.filter(from_orderID=order.id).delete()
                order.delete()
            return Response({
                "message": PrintExceptionError(err)
            }, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None, *args, **kwargs):
        logger.error("destroy order: pk {}".format(pk))
        order = Order.objects.get(pk=pk)

        if order.status != "NEW":
            return Response({
                "message": "Only NEW order can be canceled"
            }, status=status.HTTP_400_BAD_REQUEST)

        # cancel order pay by Card
        if order.payment_status == "APPROVED" and order.payment_method == "CARD":
            self.order_cancel_payment(order.payment_id)
            self.withdraw_introduction_point(pk)
            self.withdraw_self_join_point(pk)
        # cancel order pay by Point
        elif order.payment_method == "POINT":
            margin = Margin.objects.create(
                user=request.user,
                amount=order.Total,
                type="ORDER_CANCELED",
                order_type="REGULAR",
                is_refound=1,
                is_valid=True,
                from_orderID=order.id,
                fromuser=request.user
            )
            self.create_pointbank_from_margin(margin)
        # cancel order pay by MIX
        elif order.payment_status == "APPROVED" and order.payment_method == "MIX":
            self.order_cancel_payment(order.payment_id)
            logger.error("MIX order_cancel_payment")
            margin = Margin.objects.create(
                user=request.user,
                amount=order.Total - order.chargeAmount,
                type="ORDER_CANCELED",
                order_type="REGULAR",
                is_refound=1,
                is_valid=True,
                from_orderID=order.id,
                fromuser=request.user
            )
            logger.error(margin)
            self.create_pointbank_from_margin(margin)

        OrderItem.objects.filter(order=order).delete()
        Margin.objects.filter(from_orderID=order.id, order_type="REGULAR").delete()
        order.delete()

        # redis_key = settings.REDIS_KEYS["USER"]["POINTBANKS"]
        # user_redis_key = redis_key.format(request.user.id)
        # cache.delete(user_redis_key)

        return Response({
            "result": True,
            "id": pk,
            "pointbank_balance": self.pointbank_user_totalpoint(request.user.id),
            "message": "successfully deleted!",
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def set_status_completed(self, request, pk=None, *args, **kwargs):
        try:
            order = Order.objects.get(pk=pk, user=request.user)
            payment = {}

            if order.status == "DELIVERING" and order.payment_status == "APPROVED" and order.payment_id != "":
                payment = self.order_complete_payment(order.payment_id)
                order.payment_status = "COMPLETED"
                order.status = "COMPLETED"
                order.payment_info = payment["payment_details"]
                order.save()

                OrderItem.objects.filter(order=order).update(status="COMPLETED")
                Margin.objects.filter(from_orderID=order.id).update(is_valid=True)

                order_margins = Margin.objects.filter(from_orderID=order.id)
                if order_margins.exists():
                    self.create_pointbank_from_margins(order_margins)

                return Response({
                    "message": "COMPLETE order sucessfully!",
                    "order_id": pk
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "error": "Doesn't meet Compete conditions",
                }, status=status.HTTP_400_BAD_REQUEST)

        except GenerateOrderError_CreditCardFailed as err:
            return Response({
                "error_code": "creditcard_payment_complete_failed",
                "message": "Failed to complete creditcard payment"
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response({
                "error_code": "",
                "message": PrintExceptionError(err)
            }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def send_notify_email(self, request, pk=None, *args, **kwargs):
        try:
            mail_type = request.data.get("mail_type", None)
            to_supplier = request.data.get("to_supplier", None)
            to_user = request.data.get("to_user", None)

            order = Order.objects.get(pk=pk)
            if mail_type == "NEW":
                if to_supplier:
                    print("notify supplier new order")
                    if pingo_settings.SUPPLIER_AUTO_SEND_NEW_ORDERITEM_EMAIL:
                        _ids = [orderitem.id for orderitem in order.orderitems.all()]
                        if len(_ids):
                            pingo_settings.TASKS.notify_supplier_orderitem_batch(_ids)
                if to_user:
                    print("notify user new order")
                    if pingo_settings.SEND_MEMBER_NEW_ORDER_EMAIL:
                        pingo_settings.TASKS.notify_member_new_order(pk)

                print("notify superadmin new order")
                _content = f"Send {mail_type} order mail, to_user:{to_user}, to_supplier:{to_supplier}"
                pingo_settings.TASKS.common_notification(pingo_settings.ADMIN_EMAIL, _content)

            return Response(request.data, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({
                "message": PrintExceptionError(err)
            }, status=status.HTTP_400_BAD_REQUEST)


class OrderItemViewSet(DynamicQuerySetMixin, ModelViewSet):
    serializer_class = OrderItemSerializer
    model_class = OrderItem
    filters = {}
    dynamic_queryset = True
    permission_classes = (IsAuthenticated,)

    @action(detail=False, methods=["post"])
    def update_batch(self, request, *args, **kwargs):
        try:
            orderitem_ids = request.data.get("orderitem_ids", {})
            update_fields = request.data.get("update_fields", [])
            orderitems = []

            logger.error(request.data)
            if "delivery" in update_fields:
                logistic_id = request.data.get("logistic_id", None)
                delivery_info = request.data.get("delivery_info", None)
                delivered_at = request.data.get("delivered_at", None)
                delivered = request.data.get("delivered", False)

                OrderItem.objects.filter(pk__in=orderitem_ids).update(
                    delivered=delivered,
                    delivered_at=delivered_at,
                    delivery_info=delivery_info,
                    logistic_id=logistic_id,
                    status="DELIVERING" if delivered else "PROCESSING"
                )

                orderitems = OrderItem.objects.filter(pk__in=orderitem_ids)
                if delivered:
                    for _item in orderitems:
                        signalOrderItemStatusChanged.send(_item, status="DELIVERING")

            if "pay_supplier" in update_fields:
                pay_supplier_info = request.data.get("pay_supplier_info", {})
                supplier_paid = pay_supplier_info["paid"]
                OrderItem.objects.filter(pk__in=orderitem_ids).update(**pay_supplier_info)

                orderitems = OrderItem.objects.filter(pk__in=orderitem_ids)
                if supplier_paid:
                    for _item in orderitems:
                        signalOrderItemSupplierPaymentChanged.send(_item)

            serializer_orderitems = self.get_serializer(instance=orderitems, many=True)

            logger.error(request.data)
            return Response({
                "orderitems": serializer_orderitems.data
            }, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({
                "error": "ORDER_UPDATE_02",
                "message": PrintExceptionError(err),
            }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"])
    def filtered_list(self, request, *args, **kwargs):
        try:
            filters = request.data.get("filters", None)
            logger.error("filters for orderitems")
            logger.error(filters)
            orderitems_data = []
            if filters is not None:
                orderitems = OrderItem.objects.filter(**filters).order_by("-id")
                serializer = self.get_serializer(instance=orderitems, many=True)
                orderitems_data = serializer.data
            return Response({
                "results": orderitems_data
            }, status=status.HTTP_200_OK)

        except Exception as err:
            return Response({
                "message": PrintExceptionError(err),
            }, status=status.HTTP_400_BAD_REQUEST)


class InventoryViewSet(DynamicQuerySetMixin, ModelViewSet):
    serializer_class = InventorySerializer
    model_class = InventoryHistory
    dynamic_queryset = True
    filters = {}
    private_fields = "info,id"
    sorted_by = ("-id",)
    permission_classes = (StaffActionPermission,)


class MarginViewSet(DynamicQuerySetMixin, PointBankMixin, ModelViewSet):
    serializer_class = MarginSerializer
    model_class = Margin
    dynamic_queryset = True
    filters = {}
    private_fields = ""
    sorted_by = ("-created_at",)
    permission_classes = (MarginPermission,)

    @action(detail=False, methods=["get"])
    def me(self, request, *args, **kwargs):
        self.filters.update({
            "user": request.user,
            "pointbank_saved": True
        })
        return super(MarginViewSet, self).list(request, *args, **kwargs)

    def update(self, request, pk=None, *args, **kwargs):
        self.filters = {}
        update_fields = request.data.get("update_fields", None)
        if update_fields:
            request.data.pop("update_fields")

        response_data = super(MarginViewSet, self).update(request, pk, *args, **kwargs)

        margin = Margin.objects.get(pk=pk)
        if update_fields.count("is_valid"):
            self.create_pointbank_from_margin(margin)

        return response_data

    @action(methods=["post"], detail=False)
    def update_batch(self, request):
        try:
            margin_ids = request.data.get("margin_ids", [])
            update_fields = request.data.get("update_fields", [])
            if "is_valid" in update_fields:
                is_valid = request.data.get("is_valid", False)
                Margin.objects.filter(pk__in=margin_ids).update(
                    is_valid=is_valid
                )
                if is_valid:
                    margins = Margin.objects.filter(pk__in=margin_ids)
                    self.create_pointbank_from_margins(margins)

            if "amount" in update_fields:
                amount = request.data.get("amount", 0)
                Margin.objects.filter(pk__in=margin_ids).update(
                    amount=amount
                )

            margins = Margin.objects.filter(pk__in=margin_ids)
            serializer_margins = self.get_serializer(instance=margins, many=True)

            return Response({
                "margins": serializer_margins.data
            }, status=status.HTTP_200_OK)

        except Exception as err:
            return Response({
                "result": False,
                "error": "ORDER_UPDATE_02",
                "message": PrintExceptionError(err),
                "margins": {}
            }, status=status.HTTP_200_OK)


class PointBankViewSet(DynamicQuerySetMixin, PointBankMixin, ModelViewSet):
    serializer_class = PointBankSerializer
    model_class = PointBank
    dynamic_queryset = True
    filters = {}
    sorted_by = ("until_at",)
    permission_classes = (PointBankPermission,)

    @action(detail=False, methods=["get"])
    def me(self, request, *args, **kwargs):
        total_point = self.pointbank_user_totalpoint(request.user.id)
        return Response({
            "pointbank_balance": total_point
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def summary(self, request, *args, **kwargs):
        top = 0
        if "top" in self.request.query_params and int(self.request.query_params["top"]) > 0:
            top = int(self.request.query_params["top"])

        point_summary = self.pointbank_user_pointsummary(request.user.id)
        return Response({
            "point_summary": point_summary[:top] if top > 0 else point_summary,
            "pointbank_balance": self.pointbank_user_totalpoint(request.user.id)
        }, status=status.HTTP_200_OK)

    @action(methods=["post"], detail=False)
    def transfer(self, request, *args, **kwargs):
        try:

            can_transfer_point = request.user.profile.can_transfer_point
            logger.error(can_transfer_point)

            if not has_role(request.user, ["superadmin", "staff"]) and not request.user.profile.can_transfer_point:
                raise NoAccessPermission

            transfer_point = int(request.data.get("points", None))
            pre_pointbank_total = self.pointbank_user_totalpoint(user_id=request.user.id)
            if transfer_point > pre_pointbank_total:
                raise GenerateOrderError_InsufficientPoint

            data_toUserSlug = str(request.data.get("toUserSlug", None))
            toUser = User.objects.get(introcode=data_toUserSlug)
            pre_toUser_pointbank_total = self.pointbank_user_totalpoint(user_id=toUser.id)

            transfered_out_margin = Margin.objects.create(
                user=request.user,
                type="TRANSFER_OUT",
                is_valid=True,
                is_refound=-1,
                amount=transfer_point,
                from_orderID=0,
                fromuser=toUser,
                pointbank_saved=True,
                info={
                    "user_id": toUser.id,
                    "username": toUser.username}
            )
            logger.error("Created transfer out margin")
            self.pointbank_use_point(request.user, transfer_point)
            logger.error("pointbank_use_point")

            # add point to to_user
            transfered_in_margin = Margin.objects.create(
                user=toUser,
                type="TRANSFER_IN",
                is_valid=True,
                is_refound=1,
                amount=transfer_point,
                from_orderID=0,
                fromuser=request.user,
                pointbank_saved=False,
                info={"user_id": request.user.id,
                      "username": request.user.username}
            )
            logger.error("Created transfer in margin")
            self.create_pointbank_from_margin(transfered_in_margin)
            logger.error("pointbank_create_point")
            return Response({
                "data": {
                    "fromUser": {
                        "id": request.user.id,
                        "username": request.user.username,
                        "pointbank_balance": {
                            "before": pre_pointbank_total,
                            "after": self.pointbank_user_totalpoint(user_id=request.user.id)
                        }
                    },
                    "toUser": {
                        "id": toUser.id,
                        "username": toUser.username,
                        "pointbank_balance": {
                            "before": pre_toUser_pointbank_total,
                            "after": self.pointbank_user_totalpoint(user_id=toUser.id)
                        }
                    },
                    "transfer_point": transfer_point
                }
            }, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({
                "error": "TRANSFER_POINT_ERR_02",
                'message":"': 'Failed to transfer margin',
                'error_message":"': PrintExceptionError(err)
            }, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=["get"], detail=False)
    def admin_list(self, request, *arg, **kwargs):
        logger.error(request.data)
        print("admin_list self.filters")
        print(self.filters)
        return super(PointBankViewSet, self).list(request, *arg, **kwargs)
