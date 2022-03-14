from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rolepermissions.checkers import has_role
from store.models import  Margin, PointBank
from store.serializers import PointBankSerializer, MarginSerializer
from store.mixins import DynamicQuerySetMixin, PointBankMixin
from store.permissions import  PointBankPermission, MarginPermission
from pingo.exceptions import NoAccessPermission
from store.exceptions import GenerateOrderError_InsufficientPoint
from core.functions import PrintExceptionError
from django.contrib.auth import get_user_model

import logging

logger = logging.getLogger("error_logger")
User = get_user_model()


__all__ = [
    "MarginViewSet",
    "PointBankViewSet",
]


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
