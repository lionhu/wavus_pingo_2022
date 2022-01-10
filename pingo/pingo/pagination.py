from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
import logging

logger = logging.getLogger("error_logger")

DEFAULT_PAGE = 1
DEFAULT_PAGE_SIZE = 100


class CustomPagination(PageNumberPagination):
    page = DEFAULT_PAGE
    page_size = DEFAULT_PAGE_SIZE
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'total': self.page.paginator.count,
            'page': int(self.request.GET.get('page', DEFAULT_PAGE)),  # can not set default = self.page
            'page_size': int(self.request.GET.get('page_size', self.page_size)),
            'results': data
        })


class DynamicPaginationMixin(object):
    """
    Controls pagination enable disable option using query param "pagination".
    If pagination=false is passed in query params, data is returned without pagination
    """
    def paginate_queryset(self, queryset):
        pagination = self.request.query_params.get("pagination", "true")
        if pagination == "false":
            return None

        return super().paginate_queryset(queryset)
