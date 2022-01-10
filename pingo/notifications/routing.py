
from django.urls import re_path, path

from . import consumers, public_consumers

websocket_urlpatterns = [
    re_path(r'ws/notification/(?P<room_name>\w+)/$', consumers.NotificationConsumer.as_asgi()),
    path('ws/public_notification/', public_consumers.NotificationConsumer.as_asgi()),
]
