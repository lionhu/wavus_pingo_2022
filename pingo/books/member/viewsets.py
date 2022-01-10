from rest_framework import exceptions, status, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from pingo.pagination import DynamicPaginationMixin
from .serializers import BookSerializer
from books.models import Book
import logging

logger = logging.getLogger("error_logger")


class BookViewSet(DynamicPaginationMixin, viewsets.ModelViewSet):
    serializer_class = BookSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Book.objects.all()

    # both get_serializer_context and self.get_serializer can pass extra information
    # to serializer, but self.get_serializer will override get_serializer_context method
    def get_serializer_context(self):
        context = super(BookViewSet, self).get_serializer_context()
        context.update({
            "exclude_email_list": ['test@test.com', 'test1@test.com'],
            "omit_fields": ["pages",]
            # extra data
        })
        return context

    def get_queryset(self):
        # user select_related and prefetch_related to solve n+1 problem and speedup
        # return Book.objects.prefetch_related("authors").all()
        return Book.objects.select_related("publisher").all()
        # return Book.objects.prefetch_related("authors").select_related("publisher").all()

    def list(self, request, *args, **kwargs):
        logger.error("list books BookViewSet")

        # serializer = self.get_serializer(self.queryset, many=True, context={"owner": "lionhu"})
        return super(BookViewSet, self).list(request, *args, **kwargs)
