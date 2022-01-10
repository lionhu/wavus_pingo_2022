from rest_framework.decorators import action
from authentication.serializers import UserElasticSearchSerializer, ActiveUserElasticSearchSerializer, \
    ProfileElasticSearchSerializer
from core.elasticsearch import ElasticSearchViewSet
from authentication.documents import UserDocument, LoggedInUserDocument, ProfileDocument
from elasticsearch_dsl import Q as Q_elasticsearch
import logging

logger = logging.getLogger("error_logger")

__all__ = [
    "UserSearchViewSet",
    "ProfileSearchViewSet",
    "ActiveUserSearchViewSet",
]


class UserSearchViewSet(ElasticSearchViewSet):
    serializer_class = UserElasticSearchSerializer
    document_class = UserDocument
    generate_q_expression = None

    @action(methods=["get"], detail=False)
    def retrieve_children(self, request, *args, **kwargs):
        query = self.request.query_params.get("query", None)
        self.generate_q_expression = Q_elasticsearch('match', parent_introcode=query)
        return super(UserSearchViewSet, self).search(request, *args, **kwargs)


class ProfileSearchViewSet(ElasticSearchViewSet):
    serializer_class = ProfileElasticSearchSerializer
    document_class = ProfileDocument
    generate_q_expression = None

    @action(methods=["get"], detail=False)
    def retrieve_children(self, request, *args, **kwargs):
        # search by parent user id
        query = self.request.query_params.get("query", None)
        self.generate_q_expression = Q_elasticsearch('match', parent_indexing=query)
        return super(ProfileSearchViewSet, self).search(request, *args, **kwargs)


class ActiveUserSearchViewSet(ElasticSearchViewSet):
    serializer_class = ActiveUserElasticSearchSerializer
    document_class = LoggedInUserDocument
    generate_q_expression = None

    @action(methods=["get"], detail=False)
    def get_users(self, request, *args, **kwargs):
        self.generate_q_expression = Q_elasticsearch(
            "bool",
            must=[
                Q_elasticsearch("match", web=True)
            ])
        return super(ActiveUserSearchViewSet, self).search(request, *args, **kwargs)
