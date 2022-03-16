from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rolepermissions.checkers import has_role
from store.models import OrderItem,  Order, Margin
from store.serializers import OrderItemSerializer, OrderSerializer
from store.mixins import DynamicQuerySetMixin, OrderMixin, OrderPointDistribution, \
    PointBankMixin, SquarePaymentMixin
from pingo.conf import settings as pingo_settings
from store.signals import signalOrderItemStatusChanged, signalOrderItemSupplierPaymentChanged
from store.exceptions import GenerateOrderError_InsufficientPoint, GenerateOrderError_CreditCardFailed
from core.functions import PrintExceptionError
from django.contrib.auth import get_user_model

import logging

logger = logging.getLogger("error_logger")
User = get_user_model()

__all__ = [
    "OrderViewSet",
    "OrderItemViewSet"
]


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
                    pay_order_with_card = self.pay_order_byCreditCard(
                        "REGULAR", order, nonce)

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
                    holdPointInfo = self.pointbank_user_totalpoint(
                        request.user.id)
                    if cart_use_point > holdPointInfo:
                        raise GenerateOrderError_InsufficientPoint

                    pay_order_with_card = self.pay_order_byCreditCard(
                        order, nonce)

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
                    holdPointInfo = self.pointbank_user_totalpoint(
                        request.user.id)
                    logger.error("user holdPointInfo:{}, want to user point:{}".format(
                        holdPointInfo, cart_use_point))

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
                        pingo_settings.TASKS.notify_supplier_orderitem_batch(
                            _ids)

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
        Margin.objects.filter(from_orderID=order.id,
                              order_type="REGULAR").delete()
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

                OrderItem.objects.filter(
                    order=order).update(status="COMPLETED")
                Margin.objects.filter(
                    from_orderID=order.id).update(is_valid=True)

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
                        _ids = [
                            orderitem.id for orderitem in order.orderitems.all()]
                        if len(_ids):
                            pingo_settings.TASKS.notify_supplier_orderitem_batch(
                                _ids)
                if to_user:
                    print("notify user new order")
                    if pingo_settings.SEND_MEMBER_NEW_ORDER_EMAIL:
                        pingo_settings.TASKS.notify_member_new_order(pk)

                print("notify superadmin new order")
                _content = f"Send {mail_type} order mail, to_user:{to_user}, to_supplier:{to_supplier}"
                pingo_settings.TASKS.common_notification(
                    pingo_settings.ADMIN_EMAIL, _content)

            return Response(request.data, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({
                "message": PrintExceptionError(err)
            }, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=["post"], detail=False)
    def update_batch(self, request, *args, **kwargs):
        try:
            ids = request.data.get("ids", [])
            update_fields = request.data.get("update_fields", [])
            update_info = request.data.get("update_info", {})

            logger.error(request.data)
            if "status" in update_fields:
                Order.objects.filter(pk__in=ids).update(**update_info)
                
                # TODO: add tasks for different status
                
                
            # if "delivery" in update_fields:
            #     logistic_id = request.data.get("logistic_id", None)
            #     delivery_info = request.data.get("delivery_info", None)
            #     delivered_at = request.data.get("delivered_at", None)
            #     delivered = request.data.get("delivered", False)

            #     OrderItem.objects.filter(pk__in=orderitem_ids).update(
            #         delivered=delivered,
            #         delivered_at=delivered_at,
            #         delivery_info=delivery_info,
            #         logistic_id=logistic_id,
            #         status="DELIVERING" if delivered else "PROCESSING"
            #     )

            #     orderitems = OrderItem.objects.filter(pk__in=orderitem_ids)
            #     if delivered:
            #         for _item in orderitems:
            #             signalOrderItemStatusChanged.send(_item, status="DELIVERING")

            # if "pay_supplier" in update_fields:
            #     pay_supplier_info = request.data.get("pay_supplier_info", {})
            #     supplier_paid = pay_supplier_info["paid"]
            #     OrderItem.objects.filter(pk__in=orderitem_ids).update(**pay_supplier_info)

            #     orderitems = OrderItem.objects.filter(pk__in=orderitem_ids)
            #     if supplier_paid:
            #         for _item in orderitems:
            #             signalOrderItemSupplierPaymentChanged.send(_item)

            # serializer_orderitems = self.get_serializer(instance=orderitems, many=True)

            logger.error(request.data)
            return Response({
                "ids": ids
            }, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({
                'error': 'UpdateBatch_Err01',
                'message': PrintExceptionError(err)
            }, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None, *args, **kwargs):
        try:
            print(request.data)
            update_fields = request.data.get("update_fields", None)

            if update_fields is None:
                return Response({
                    "error": "ORDER_UPDATE_01",
                    "message": "update_fields is required",
                }, status=status.HTTP_400_BAD_REQUEST)

            update_info = request.data.get("update_info", {})
            Order.objects.filter(pk=pk).update(**update_info)

            if "delivery" in update_fields:
                update_info = request.data.get("update_info", None)
                if update_info and update_info["delivered"]:
                    if pingo_settings.NOTIFICATIONS["USER_ORDER_DELIVERED"]:
                        pingo_settings.TASKS.notify_member_order_delivered(pk, update_info)

                    if pingo_settings.NOTIFICATIONS["SUPERADMIN_ORDER_DELIVERED"]:
                        pingo_settings.TASKS.notify_superadmin_order_delivered(pk, update_info)

            if "status" in update_fields:
                _status = update_info["status"]
                print(f"status update_fields {_status}")
                # if _status == "PROCESSING":
                #     pingo_settings.TASKS.notify_supplier_order(pk)

            return Response({
                "order_id": pk
            }, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({
                "error": "ORDER_UPDATE_02",
                "message": PrintExceptionError(err),
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
