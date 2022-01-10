from rest_framework.decorators import action
from rest_framework.response import Response
from store.serializers import ItemElasticSearchSerializer, PointBankElasticSearchSerializer, \
    FavoriteElasticSearchSerializer, ViewProductHistoryElasticSearchSerializer, CommentElasticSearchSerializer, \
    VariationElasticSearchSerializer
from core.elasticsearch import ElasticSearchViewSet
from store.documents import ProductDocument, PointBankDocument, FavoriteDocument, ViewProductHistoryDocument, \
    ProductCommentDocument, VariationDocument
from store.models import Favorite
import numpy as np
from elasticsearch_dsl import Q as Q_elasticsearch
from core.charts import objects_to_df, Chart, filter_objects
from pingo.conf import settings as pingo_settings
import logging

logger = logging.getLogger("error_logger")
PALETTE = ['#465b65', '#184c9c', '#d33035', '#ffc107', '#28a745', '#6f7f8c', '#6610f2', '#6e9fa5', '#fd7e14', '#e83e8c',
           '#17a2b8', '#6f42c1']

__all__ = [
    "FilterCommentsViewSet",
    "FilterViewProductHistoriesViewSet",
    "FilterFavoritesViewSet",
    "FilterPointBanksViewSet",
    "FilterProductsViewSet",
    "FilterVariationsViewSet",
]


class FilterCommentsViewSet(ElasticSearchViewSet):
    serializer_class = CommentElasticSearchSerializer
    document_class = ProductCommentDocument
    generate_q_expression = None

    @action(methods=["get"], detail=False)
    def me(self, request, *args, **kwargs):
        query = self.request.query_params.get("query", None)
        self.generate_q_expression = Q_elasticsearch('match', user__id=query)
        return super(FilterCommentsViewSet, self).search(request, *args, **kwargs)

    @action(methods=["get"], detail=False)
    def all(self, request, *args, **kwargs):
        approved = self.request.query_params.get("approved", None)
        checked = self.request.query_params.get("checked", None)
        self.generate_q_expression = Q_elasticsearch(
            'bool',
            must=[
                Q_elasticsearch('match', approved=approved),
                Q_elasticsearch('match', checked=checked)
            ])

        return super(FilterCommentsViewSet, self).search(request, *args, **kwargs)

    @action(methods=["get"], detail=False)
    def of_product(self, request, *args, **kwargs):
        query = self.request.query_params.get("query", None)
        self.generate_q_expression = Q_elasticsearch('match', item__id=query)
        return super(FilterCommentsViewSet, self).search(request, *args, **kwargs)


class FilterViewProductHistoriesViewSet(ElasticSearchViewSet):
    serializer_class = ViewProductHistoryElasticSearchSerializer
    document_class = ViewProductHistoryDocument
    generate_q_expression = None

    @action(methods=["get"], detail=False)
    def me(self, request, *args, **kwargs):
        query = self.request.query_params.get("query", None)

        self.generate_q_expression = Q_elasticsearch(
            'bool',
            must=[
                Q_elasticsearch('match', user__id=query),
                Q_elasticsearch('match', item__is_valid=True)
            ])
        return super(FilterViewProductHistoriesViewSet, self).search(request, *args, **kwargs)


class FilterFavoritesViewSet(ElasticSearchViewSet):
    serializer_class = FavoriteElasticSearchSerializer
    document_class = FavoriteDocument
    generate_q_expression = None

    @action(methods=["get"], detail=False)
    def me(self, request, *args, **kwargs):
        query = self.request.query_params.get("query", None)
        self.generate_q_expression = Q_elasticsearch(
            'bool',
            must=[
                Q_elasticsearch('match', user__id=query),
                Q_elasticsearch('match', item__is_valid=True)]
        )
        return super(FilterFavoritesViewSet, self).search(request, *args, **kwargs)

    @action(methods=["get"], detail=False)
    def all(self, request, *args, **kwargs):
        self.generate_q_expression = Q_elasticsearch(
            'range', id={"gte": 0}
        )
        return super(FilterFavoritesViewSet, self).search(request, *args, **kwargs)

    @action(methods=["get"], detail=False)
    def ranking(self, request, *args, **kwargs):
        # self.generate_q_expression = Q_elasticsearch(
        #     'range', id={"gte": 0}
        # )
        # pkl = self.search_data(request, *args, **kwargs)
        # print(pkl)
        # return Response({}, 200)
        top_n = request.data.get("query", 10)
        mychart = Chart(palette=PALETTE)
        margins_qs = filter_objects(Favorite, fields=["item"], foreign_info=["item_name", "item__item_name"])

        print(margins_qs)
        margin_summary = {"labels": [], "datasets": []}
        if margins_qs.count():
            df_margins = objects_to_df(margins_qs, fields=["item", "item_name"])
            df_margins["counts"] = 1
            mychart.from_df_topranking(df_margins, values=['counts'], labels=['item_name'],
                                       aggfunc=np.sum, sort_by="counts")
            margin_summary = mychart.get_presentation()
        return Response({"margin_summary": margin_summary}, 200)


class FilterPointBanksViewSet(ElasticSearchViewSet):
    serializer_class = PointBankElasticSearchSerializer
    document_class = PointBankDocument
    generate_q_expression = None

    @action(methods=["get"], detail=False)
    def me(self, request, *args, **kwargs):
        query = self.request.query_params.get("query", None)
        self.generate_q_expression = Q_elasticsearch('match', user__username=query)
        return super(FilterPointBanksViewSet, self).search(request, *args, **kwargs)


class FilterProductsViewSet(ElasticSearchViewSet):
    serializer_class = ItemElasticSearchSerializer
    document_class = ProductDocument
    generate_q_expression = None

    @action(methods=["get"], detail=False)
    def valid(self, request, *args, **kwargs):
        self.generate_q_expression = Q_elasticsearch('match', is_valid=True)
        return super(FilterProductsViewSet, self).search(request, *args, **kwargs)

    @action(methods=["get"], detail=False)
    def ofLabel(self, request, *args, **kwargs):
        query = self.request.query_params.get("query", None)
        # self.generate_q_expression = Q_elasticsearch('match', labels=query)
        self.generate_q_expression = Q_elasticsearch(
            'bool',
            must=[
                Q_elasticsearch('match', labels=query),
                Q_elasticsearch('match', is_valid=True)
            ])
        return super(FilterProductsViewSet, self).search(request, *args, **kwargs)

    @action(methods=["get"], detail=True)
    def ofCategory(self, request, pk=None, *args, **kwargs):
        category_id = int(pk)
        if category_id > 0:
            self.generate_q_expression = Q_elasticsearch(
                'bool',
                must=[
                    Q_elasticsearch('match', category__id=category_id),
                    Q_elasticsearch('match', is_valid=True)
                ])
            return super(FilterProductsViewSet, self).search(request, *args, **kwargs)
        else:
            return self.valid(request, *args, **kwargs)

    @action(methods=["get"], detail=False)
    def by_name_description(self, request, *args, **kwargs):
        query = self.request.query_params.get("query", None)
        self.generate_q_expression = Q_elasticsearch(
            'multi_match', query=query,
            fields=[
                'item_name',
                'description',
            ], fuzziness='auto')

        return super(FilterProductsViewSet, self).search(request, *args, **kwargs)

    @action(methods=["get"], detail=False)
    def by_id(self, request, *args, **kwargs):
        query = self.request.query_params.get("query", None)
        self.generate_q_expression = Q_elasticsearch(
            'match', id=query)

        return super(FilterProductsViewSet, self).search(request, *args, **kwargs)


class FilterVariationsViewSet(ElasticSearchViewSet):
    serializer_class = VariationElasticSearchSerializer
    document_class = VariationDocument
    generate_q_expression = None

    @action(methods=["get"], detail=True)
    def ofProduct(self, request, pk=None, *args, **kwargs):
        item_id = int(pk)
        if item_id > 0:
            self.generate_q_expression = Q_elasticsearch(
                'bool',
                must=[
                    Q_elasticsearch('match', item__id=item_id),
                ])
            return super(FilterVariationsViewSet, self).search(request, *args, **kwargs)
        else:
            return self.valid(request, *args, **kwargs)

    @action(methods=["get"], detail=False)
    def ofCategory(self, request, *args, **kwargs):
        query = self.request.query_params.get("query", None)
        self.generate_q_expression = Q_elasticsearch(
            'bool',
            must=[
                Q_elasticsearch('match', item__category_indexing=query),
            ])
        return super(FilterVariationsViewSet, self).search(request, *args, **kwargs)

    @action(methods=["get"], detail=False)
    def by_name_description(self, request, *args, **kwargs):
        query = self.request.query_params.get("query", None)
        self.generate_q_expression = Q_elasticsearch(
            'multi_match', query=query,
            fields=[
                'item_name',
                'description',
            ], fuzziness='auto')

        return super(FilterVariationsViewSet, self).search(request, *args, **kwargs)

    @action(methods=["get"], detail=True)
    def by_id(self, request, pk=None, *args, **kwargs):
        self.generate_q_expression = Q_elasticsearch(
            'match', id=pk)

        return super(FilterVariationsViewSet, self).search(request, pk, *args, **kwargs)
