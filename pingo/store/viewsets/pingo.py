from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.utils.timezone import make_aware
from store.models import Margin, PingoItem, PingoOrder, PingoItemSliderImage, Logistic
from store.serializers import PingoItemSerializer, PingoOrderSerializer, PingoItemSliderImageSerializer
from store.mixins import DynamicQuerySetMixin, OrderMixin, OrderPointDistribution, \
    PointBankMixin, SquarePaymentMixin
from core.functions import PrintExceptionError, generate_user_product_qr, extract_query_param_filter
from core.mixins import RedisMixin
from pingo.permissions import StaffActionPermission, SAFEActionPermission
from store.permissions import PingoProductPermission, CommentPermission
from pingo.conf import settings as pingo_settings
from rolepermissions.checkers import has_role
from django.core.cache import cache
from datetime import datetime
from django.contrib.auth import get_user_model

import logging

logger = logging.getLogger("error_logger")
User = get_user_model()


class PingoItemSliderImageViewSet(DynamicQuerySetMixin, ModelViewSet):
    serializer_class = PingoItemSliderImageSerializer
    permission_classes = (SAFEActionPermission,)
    model_class = PingoItemSliderImage
    dynamic_queryset = True
    filters = {}


class PingoProductViewSet(DynamicQuerySetMixin, RedisMixin, PointBankMixin, SquarePaymentMixin, ModelViewSet):
    serializer_class = PingoItemSerializer
    model_class = PingoItem
    dynamic_queryset = True
    filters = {}
    private_fields = ""
    sorted_by = ("-until_at",)
    permission_classes = (PingoProductPermission,)

    @action(detail=True, methods=["post"])
    def update_post_image(self, request, pk=None, *args, **kwargs):
        item = PingoItem.objects.get(pk=pk)
        image = request.data.get("image", None)
        if image is not None:
            item.image = image
            item.save()
            return super(PingoProductViewSet, self).retrieve(request, pk, *args, **kwargs)
        return Response({}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        if not has_role(request.user, ["superadmin", "staff"]):
            self.filters = {"is_valid": True}

        return super(PingoProductViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, pk=None, *args, **kwargs):
        # if not request.user.is_anonymous:
        #     recore_viewproduct_event.delay(user_id=request.user.id, item_id=pk, type="PINGO")
        if not has_role(request.user, ["superadmin", "staff"]):
            self.filters = {"is_valid": True}

        prefix_redis = f"pingo_product_{pk}"
        cached_data = self.get_redis_data(prefix_redis, request)

        if pingo_settings.USE_REDIS_CACHE:
            if cached_data is None:
                response = super(self.__class__, self).retrieve(request, pk, *args, **kwargs)
                cached_data = response.data
                self.set_redis_data(prefix_redis, request, cached_data, 300)
        else:
            response = super(self.__class__, self).retrieve(request, pk, *args, **kwargs)
            cached_data = response.data

        return Response(cached_data, status=status.HTTP_200_OK)

    def update(self, request, pk=None, *args, **kwargs):
        cache.delete_pattern(f"*pingo_product_{pk}*")
        cache.delete_pattern(f"*shop_categories*")
        return super(PingoProductViewSet, self).update(request, pk, *args, **kwargs)

    @action(detail=False, methods=["get"])
    def list_recruiting(self, request, *args, **kwargs):
        aware_time = make_aware(datetime.now())
        self.filters = {
            "is_valid": True,
            "status": "RECRUITING",
            "until_at__gte": aware_time,
        }

        prefix_redis = f"pingo_products_recruiting_{aware_time}"
        cached_data = self.get_redis_data(prefix_redis, request)

        if pingo_settings.USE_REDIS_CACHE:
            if cached_data is None:
                response = super(self.__class__, self).list(request, *args, **kwargs)
                cached_data = response.data
                self.set_redis_data(prefix_redis, request, cached_data, 300)
        else:
            response = super(self.__class__, self).list(request, *args, **kwargs)
            cached_data = response.data

        return Response(cached_data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"])
    def get_introduce_qr(self, request, pk=None):
        try:
            product = PingoItem.objects.get(pk=pk)
            share_code_data = generate_user_product_qr(request.user, product, "tomobuy")
            return Response(share_code_data, status=status.HTTP_200_OK)

        except Exception as err:
            return Response({
                'error_message":"': PrintExceptionError(err)
            }, status=status.HTTP_200_OK)

    @action(methods=["post"], detail=True)
    def establish_pingoitem(self, request, pk=None, *args, **kwargs):
        try:
            pingoitem = PingoItem.objects.get(pk=pk)
            pingoOrders = PingoOrder.objects.filter(product=pingoitem)

            result_ids = []
            for order in pingoOrders:
                if order.payment_method == "CARD" and order.payment_id != "" and order.payment_status == "APPROVED":
                    opt_cancel = self.order_complete_payment(order.payment_id)

                    order.payment_status = opt_cancel["payment_status"]
                    order.payment_info = opt_cancel["payment_details"]

                    Margin.objects.filter(from_orderID=order.id, order_type="PINGO").update(is_valid=True)
                    margins = Margin.objects.filter(from_orderID=order.id, order_type="PINGO")
                    self.create_pointbank_from_margins(margins)

                result_ids.append(order.id)
                order.status = "ESTABLISHED"
                order.save()

                # notify order buyer

            pingoitem.status = "ESTABLISHED"
            pingoitem.save()

            # notify pingoitem vendor and superadmin

            cache.delete_pattern(f"*pingo_product_{pingoitem.id}*")
            cache.delete_pattern(f"*shop_categories*")
            return Response({
                "result_ids": result_ids
            }, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({
                "message": PrintExceptionError(err)
            }, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=["post"], detail=True)
    def release_pingoitem(self, request, pk=None, *args, **kwargs):
        try:
            pingoitem = PingoItem.objects.get(pk=pk)
            pingoOrders = PingoOrder.objects.filter(product=pingoitem)

            result_ids = []
            for order in pingoOrders:
                if order.payment_method == "CARD" and order.payment_id != "" and order.payment_status == "APPROVED":
                    opt_cancel = self.order_cancel_payment(order.payment_id)
                    order.payment_status = opt_cancel["payment_status"]
                    order.payment_info = opt_cancel["payment_details"]
                elif order.payment_method == "POINT":
                    self.refound_canceled_pingoOrder(order)

                Margin.objects.filter(from_orderID=order.id, order_type="PINGO").delete()
                result_ids.append(order.id)
                order.status = "RELEASED"
                order.save()

                # notify order buyer

            pingoitem.status = "RELEASED"
            pingoitem.save()

            # notify pingoitem vendor and superadmin

            cache.delete_pattern(f"*pingo_product_{pingoitem.id}*")
            cache.delete_pattern(f"*shop_categories*")
            return Response({
                "result_ids": result_ids
            }, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({
                "message": PrintExceptionError(err)
            }, status=status.HTTP_400_BAD_REQUEST)


class PingoOrderViewSet(DynamicQuerySetMixin, PointBankMixin, OrderMixin,
                        SquarePaymentMixin, ModelViewSet):
    serializer_class = PingoOrderSerializer
    model_class = PingoOrder
    dynamic_queryset = True
    filters = {}
    sorted_by = ("-created_at",)
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        pingo_order = None
        try:
            message = "Not access permission"
            if has_role(request.user, ["superadmin", "staff", "supplier"]):
                return Response({
                    "message": message
                }, status=status.HTTP_403_FORBIDDEN)

            payment_method = request.data.get("payment_method", "CARD")
            nonce = request.data.get("nonce", None)
            chargeAmount = request.data.get("chargeAmount", 0)
            request.data["user"] = request.user.id

            # Payment creditcard
            if payment_method == "CARD":
                if chargeAmount and nonce:
                    order_serializer = self.get_serializer(data=request.data)
                    if order_serializer.is_valid(raise_exception=True):
                        logger.error("payment OK")
                        pingo_order = order_serializer.save()

                        pay_order_with_card = self.pay_order_byCreditCard("PINGO", pingo_order, nonce)
                        pingo_order.payment_info = pay_order_with_card["payment_details"]
                        pingo_order.payment_status = pay_order_with_card["payment_status"]
                        pingo_order.payment_id = pay_order_with_card["payment_id"]
                        pingo_order.is_paid = True
                        pingo_order.save()

                        # signalPingoProductCurrentChanged.send(pingo_product)

                        order_point_distributor = OrderPointDistribution(pingo_order)
                        order_point_distributor.distribute_pingoOrder_point()

                        # self.notify_user(request, pingo_order.id)

                        return Response({
                            "result": True,
                            "operation": "create",
                            "pointbank_balance": self.pointbank_user_totalpoint(request.user.id)
                        }, status=status.HTTP_200_OK)
                    else:
                        if pingo_order is not None:
                            pingo_order.delete()

                cache.delete_pattern(f"*pingo_product_{pingo_order.product.id}*")
                return Response({
                    "error_code": "pingo_order_param_error01",
                    "message": "Failed to apply credit card payment",
                }, status=status.HTTP_400_BAD_REQUEST)

            else:
                # Payment Point
                holdPointInfo = self.pointbank_user_totalpoint(request.user.id)
                if holdPointInfo >= chargeAmount:
                    self.pointbank_use_point(request.user.id, chargeAmount)

                    order_serializer = self.get_serializer(data=request.data)
                    if order_serializer.is_valid(raise_exception=True):
                        logger.error("Point payment OK")
                        pingo_order = order_serializer.save()

                        Margin.objects.create(
                            type="PURCHASE_ORDER",
                            order_type="PINGO",
                            user=request.user,
                            fromuser=request.user,
                            amount=chargeAmount,
                            is_valid=True,
                            is_refound=-1,
                            from_orderID=pingo_order.id,
                            pointbank_saved=True,
                            info={"order_id": pingo_order.id}
                        )

                        # signalPingoProductCurrentChanged.send(pingo_product)

                        # self.notify_user(request, pingo_order.id)

                        return Response({
                            "result": True,
                            "operation": "create",
                            "pointbank_balance": self.pointbank_user_totalpoint(request.user.id)
                        }, status=status.HTTP_200_OK)
                return Response({
                    "error_code": "pingo_order_param_error02",
                    "message": "Failed to apply point payment",
                }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as err:
            return Response({
                "message": PrintExceptionError(err)
            }, status=status.HTTP_400_BAD_REQUEST)

    def destroy_point_order(self, request, pingo_order):
        try:
            use_point = int(pingo_order.point_usage["use_point"])
            pingo_product_id = pingo_order.product.id

            if pingo_order.point_usage["apply_point"] and use_point > 0:
                margin = Margin.objects.create(
                    type="PURCHASE_ORDER",
                    order_type="PINGO",
                    user=request.user,
                    fromuser=request.user,
                    amount=use_point,
                    is_valid=True,
                    is_refound=1,
                    from_orderID=pingo_order.id,
                    pointbank_saved=False,
                    info={"order_id": pingo_order.id}
                )
                self.create_pointbank_from_margin(margin)
                # task_RemovePingoOrder.delay(pingo_order.id)

                # signalPingoProductCurrentChanged.send(pingo_order.product)
                Margin.objects.filter(from_orderID=pingo_order.id, order_type="PINGO").delete()
                pingo_order.delete()
                cache.delete_pattern(f"*pingo_product_{pingo_product_id}*")
        except Exception as err:
            return Response({
                "message": PrintExceptionError(err)
            }, status=status.HTTP_404_NOT_FOUND)

    def destroy_card_order(self, request, pingo_order):
        try:
            pingo_product_id = pingo_order.product.id

            if pingo_order.payment_status == "APPROVED" and pingo_order.payment_id != "":
                self.order_cancel_payment(pingo_order.payment_id)

            Margin.objects.filter(from_orderID=pingo_order.id, order_type="PINGO").delete()
            pingo_order.delete()
            cache.delete_pattern(f"*pingo_product_{pingo_product_id}*")
        except Exception as err:
            return Response({
                "message": PrintExceptionError(err)
            }, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None, *args, **kwargs):
        try:
            pingo_order = PingoOrder.objects.get(pk=pk, user=request.user)
            if pingo_order.status != "RECRUITING":
                return Response({
                    "error_code": "not_RECRUITING_order"
                }, status=status.HTTP_400_BAD_REQUEST)

            if pingo_order.payment_method == "POINT":
                self.destroy_point_order(request, pingo_order)

            elif pingo_order.payment_method == "CARD":
                self.destroy_card_order(request, pingo_order)

            return Response({
                "payment_method": pingo_order.payment_method,
                "id": pk,
                "pointbank_balance": self.pointbank_user_totalpoint(request.user.id)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response({
                "message": PrintExceptionError(err)
            }, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=["get"], detail=False)
    def me(self, request, *args, **kwargs):
        self.filters = {
            "user": request.user
        }
        return super(PingoOrderViewSet, self).list(request, *args, **kwargs)

    @action(methods=["post"], detail=False)
    def destroy_batch(self, request):
        try:
            ids = request.data.get("ids", None)
            result_ids = []
            logger.error("destroy batch orders")
            logger.error(ids)

            orders = PingoOrder.objects.filter(pk__in=ids)

            for order in orders:
                if order.payment_method == "CARD":
                    self.destroy_card_order(request, order)
                elif order.payment_method == "POINT":
                    self.destroy_point_order(request, order)
                result_ids.append(order.id)

            return Response({
                "result_ids": result_ids
            }, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({
                "message": PrintExceptionError(err)
            }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def update_batch(self, request, *arg, **kwargs):
        try:
            logger.error(request.data)

            order_ids = request.data.get("orderitem_ids", {})
            update_fields = request.data.get("update_fields", [])
            if "delivery" in update_fields:
                logistic_id = request.data.get("logistic_id", None)
                # logistic = Logistic.objects.get(pk=logistic_id)
                delivery_info = request.data.get("delivery_info", None)
                delivered_at = request.data.get("delivered_at", None)
                delivered = request.data.get("delivered", False)

                PingoOrder.objects.filter(pk__in=order_ids).update(
                    delivered=delivered,
                    delivered_at=delivered_at,
                    delivery_info=delivery_info,
                    logistic_id=logistic_id,
                    status="DELIVERING" if delivered else "PROCESSING"
                )
                # extra_data["logistic"] = LogisticSerializer(logistic, many=False).data

                # orders = PingoOrder.objects.filter(pk__in=order_ids)
                # if delivered:
                #     for _order in orders:
                #         pass
                # send delivery info to buyer?
                # signalOrderItemStatusChanged.send(_order, status="DELIVERING")
                return Response({
                    "message": "updated successfully!",
                }, status=status.HTTP_200_OK)

            return Response({
                "result": True,
                "message": "updated successfully!",
            }, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({
                "error": "ORDER_UPDATE_02",
                "message": PrintExceptionError(err),
            }, status=status.HTTP_400_BAD_REQUEST)

    # @action(methods=["get"], detail=True)
    # def download_product_orders(self, request, pk=None,*arg,**kwargs):
    #
    #     qs = PingoOrder.objects.filter(product_id=pk)
    #     if qs.exists():
    #         csv_buffer = qs_to_csv(qs, json_fields=["json_shippingaddress", "delivery_info"],
    #                                exclude_fields=["json_variant", "json_product", "point_usage"])
    #         response = HttpResponse(csv_buffer, content_type='text/csv')
    #         response['Content-Disposition'] = 'attachment; filename=pingo_orders.csv'
    #         return response
