from django.urls import path, include
from rest_framework.routers import DefaultRouter
from backend_admin.viewsets import DashboardViewSet, SystemViewSet
from store.viewsets import CategoryViewSet, SupplierViewSet, ProductViewSet

app_name = 'backend_admin'

router = DefaultRouter()
router.register('dashboard', DashboardViewSet, basename="dashboard")
router.register('system', SystemViewSet, basename="system")
router.register("categories", CategoryViewSet, basename="categories")
router.register('suppliers', SupplierViewSet, basename="suppliers")
router.register("products", ProductViewSet, basename="products")

urlpatterns = [
    path("", include((router.urls, "backend_admin"), namespace="backend_admin")),
]
