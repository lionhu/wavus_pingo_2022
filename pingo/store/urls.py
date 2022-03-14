from django.urls import path, include
from rest_framework.routers import DefaultRouter
from store.viewsets import CategoryViewSet, SectionViewSet, FaqViewSet, LogisticViewSet, \
    SupplierViewSet, AddressBookViewSet, ProductViewSet, VariationViewSet, \
    ItemSliderImageViewSet, ViewProductHistoryViewSet, CommentViewSet, ThumbsViewSet, \
    FavoriteViewSet, OrderItemViewSet, InventoryViewSet, OrderViewSet, PointBankViewSet, \
    MarginViewSet, SystemViewSet, PingoProductViewSet, PingoOrderViewSet, PingoItemSliderImageViewSet, \
    FilterProductsViewSet, FilterPointBanksViewSet, FilterFavoritesViewSet, \
    FilterViewProductHistoriesViewSet, FilterCommentsViewSet, FilterVariationViewSet
from .views import download_csv

app_name = 'store'

router = DefaultRouter()
router.register("categories", CategoryViewSet, basename="categories")
router.register("faqs", FaqViewSet, basename="faqs")
router.register("logistics", LogisticViewSet, basename="logistics")
router.register('sections', SectionViewSet, basename="sections")
router.register('suppliers', SupplierViewSet, basename="suppliers")
router.register('addressbooks', AddressBookViewSet, basename="addressbooks")
router.register('products', ProductViewSet, basename="products")
router.register('pingo_products', PingoProductViewSet, basename="pingo_products")
router.register('variations', VariationViewSet, basename="variations")
router.register('sliderimages', ItemSliderImageViewSet, basename="sliderimages")
router.register('pingo_sliderimages', PingoItemSliderImageViewSet, basename="pingo_sliderimages")
router.register('viewproducthistory', ViewProductHistoryViewSet, basename="viewproducthistory")
router.register('comments', CommentViewSet, basename="comments")
router.register('thumbs', ThumbsViewSet, basename="thumbs")
router.register('favorites', FavoriteViewSet, basename="favorites")
router.register('orderitems', OrderItemViewSet, basename="orderitems")
router.register('inventory', InventoryViewSet, basename="inventory")
router.register('orders', OrderViewSet, basename="orders")
router.register('pingo_orders', PingoOrderViewSet, basename="pingo_orders")
router.register('pointbanks', PointBankViewSet, basename="pointbanks")
router.register('margins', MarginViewSet, basename="margins")
router.register('system', SystemViewSet, basename="system")
router.register("filter_products", FilterProductsViewSet, basename="filter_products")
router.register("filter_variations", FilterVariationViewSet,basename="filter_variations")
router.register("filter_pointbanks", FilterPointBanksViewSet, basename="filter_pointbanks")
router.register("filter_favorites", FilterFavoritesViewSet, basename="filter_favorites")
router.register("filter_viewproducts", FilterViewProductHistoriesViewSet, basename="filter_viewproducts")
router.register("filter_comments", FilterCommentsViewSet, basename="filter_comments")

from .views import HelloPDFView

urlpatterns = [
    path("public/", include((router.urls, "store"), namespace="pingo_shop")),
    path('export_pdf/<str:order_type>/<uuid:slug>/', HelloPDFView, name="export_order_pdf"),
    path('<int:supplier_id>/download_csv/<str:ordered_at__gte>/<str:ordered_at__lte>/', download_csv,
         name="download_csv"),
]
