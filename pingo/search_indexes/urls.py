from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from .viewsets import BookDocumentViewSet

router = DefaultRouter()
books = router.register(r'books',
                        BookDocumentViewSet,
                        basename='bookdocument')
urlpatterns = [
    url(r'^', include(router.urls)),
]
