from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from .member.viewsets import BookViewSet

router = DefaultRouter()
books = router.register(r'books',BookViewSet, basename='books')

urlpatterns = [
    url(r'^', include(router.urls)),
]
