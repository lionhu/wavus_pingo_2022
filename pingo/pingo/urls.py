from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include
from search_indexes import urls as search_index_urls
import debug_toolbar

from rest_framework import routers

# from core.viewsets import UserViewSet
# 单独导入定制信息后的token
# from core.views import PingoTokenObtainPairView
# from rest_framework_simplejwt.views import TokenRefreshView
# router = routers.DefaultRouter()
# router.register(r'users', UserViewSet)

admin.site.site_header = "海光楽園へようこそ！"
admin.site.index_title = "管理ホーム"
admin.site.site_url = "https://www.pingo.jp"

urlpatterns = [
    path('daphne/', include([
        path('admin/', admin.site.urls),

        path('api/backend/', include([
            path('', include('backend_admin.urls')),  # add
        ])),
        path('api/', include([
            path('auth/', include('djoser.urls.jwt')),  # add
            # path('auth/', include('djoser.urls.authtoken')),  # add
            path('auth/', include('authentication.urls')),  # add
            path('search/', include(search_index_urls)),  # add
            path('bookstore/', include('books.urls')),  # add
            path('store/', include('store.urls')),  # add
        ])),

    ])),
    path('chat/', include('chat.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
