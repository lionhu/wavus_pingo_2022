from django.contrib.auth import get_user_model
from rest_framework.routers import DefaultRouter
from django.urls import include
from django.urls import path
from authentication.viewsets import PingoUserViewSet, ClientViewSet, TokenObtainPairView, TokenRefreshView, \
    ProfileViewSet, SearchUsers, UserSearchViewSet, ActiveUserSearchViewSet, ProfileSearchViewSet

router = DefaultRouter()
router.register("users", PingoUserViewSet, basename="users")
router.register("clients", ClientViewSet, basename="clients")
router.register("profiles", ProfileViewSet, basename="profiles")
router.register("search_users", UserSearchViewSet, basename="search_users")
router.register("search_active_users", ActiveUserSearchViewSet, basename="search_active_users")
router.register("search_profiles", ProfileSearchViewSet, basename="search_profiles")

User = get_user_model()

# urlpatterns = router.urls
urlpatterns = [
    path("", include((router.urls, "api_auth"), namespace="api_auth")),
    path('token/obtain/', TokenObtainPairView.as_view(), name='token-obtain'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path("search_users/<str:query>/", SearchUsers.as_view(), name="search_users")
]
