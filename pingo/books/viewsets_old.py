from rest_framework import exceptions, status, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_elasticsearch_dsl_drf.pagination import PageNumberPagination
from .serializers import BookSerializer
from .models import Book


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10

    def get_paginated_response_context(self, data):
        __data = super(CustomPageNumberPagination, self).get_paginated_response_context(data)
        __data.append(('current_page', int(self.request.query_params.get('page', 1))))
        __data.append(('page_size', self.get_page_size(self.request)))

        return sorted(__data)


class BookViewSet(viewsets.ModelViewSet):
    serializer_class = BookSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Book.objects.all()
    pagination_class = CustomPageNumberPagination
