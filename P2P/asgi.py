
import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from accounts import *
from contact import *
from currency import *
from payment import *
from chat.routings import websocket_urlpatterns

from P2P.settings import CHANNEL_LAYERS


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'P2P.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})

# Use pre-defined channel layer
channel_layer = CHANNEL_LAYERS['redis']
