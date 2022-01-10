from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
import logging
from store.models import PointBank, Margin, ViewProductHistory, OrderItem, Order, \
    Logistic, ViewProductHistory, InventoryHistory, Category, Item, \
    Section, Faq, Supplier, ItemSliderImage, Variation, PingoOrder, PingoItem
from pingo.permissions import (IsSuperAdmin, IsStaff, IsObjectOwner, IsSupplier, StaffActionPermission,
                               SAFEActionPermission)
from core.charts import objects_to_df, Chart, filter_objects
from core.functions import PrintExceptionError

User = get_user_model()
logger = logging.getLogger("error_logger")
CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)
PALETTE = ['#465b65', '#184c9c', '#d33035', '#ffc107', '#28a745', '#6f7f8c', '#6610f2', '#6e9fa5', '#fd7e14', '#e83e8c',
           '#17a2b8', '#6f42c1']

__all__ = [
    "DashboardViewSet",
]


class DashboardViewSet(GenericViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly, IsSuperAdmin)

    @action(detail=False, methods=["get"])
    def get_charts(self, request):
        try:
            mychart = Chart(palette=PALETTE)
            margins_qs = filter_objects(Margin, fields=["amount", "type", "created_at"],
                                        is_refound=1, pointbank_saved=False)
            margin_summary = {"labels": [], "datasets": []}
            if margins_qs.count():
                df_margins = objects_to_df(margins_qs, fields=["amount", "type", "created_at"],
                                           date_cols=["%y-%m", "created_at"])
                mychart.from_df_topranking(df_margins, values='amount', labels=['type'], sort_by="amount")
                margin_summary = mychart.get_presentation()

            user_margin_summary_qs = filter_objects(Margin, fields=["amount", "type", "created_at"],
                                                    foreign_info=["username", "user__username"], is_refound=1,
                                                    pointbank_saved=False)
            user_margin_summary = {"labels": [], "datasets": []}
            if user_margin_summary_qs.count():
                df_user_margin_summary = objects_to_df(user_margin_summary_qs,
                                                       fields=["amount", "type", "created_at", "username"],
                                                       date_cols=["%y-%m", "created_at"])
                mychart.from_df(df_user_margin_summary, values='amount', labels=['username'], stacks="type",
                                sort_by="All", Top_n=3,
                                df_type="Table", margins=True)
                user_margin_summary = mychart.get_presentation()

            user_ranking_qs = filter_objects(PointBank, fields=["point"], foreign_info=["username", "user__username"])
            user_ranking = {"labels": [], "datasets": []}
            if user_ranking_qs.count():
                df_user_ranking = objects_to_df(user_ranking_qs, fields=["point", "username"])
                mychart.from_df(df_user_ranking, values="point", labels="username", sort_by="point", Top_n=3,
                                df_type="Ranking")
                user_ranking = mychart.get_presentation()

            return Response({
                "margin_summary": margin_summary,
                "user_margin_summary": user_margin_summary,
                "user_ranking": user_ranking
            }, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({
                "message": PrintExceptionError(err)
            }, status=status.HTTP_400_BAD_REQUEST)
