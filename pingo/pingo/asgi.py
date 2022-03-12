import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
django_asgi_app = get_asgi_application()


import notifications.routing
from authentication.middlewares import TokenAuthMiddleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hello_daphne.settings')
application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": TokenAuthMiddleware(
        # URLRouter(
        #     chat.routing.websocket_urlpatterns,
        # ),
        URLRouter(
            notifications.routing.websocket_urlpatterns,
        )
    ),
})
