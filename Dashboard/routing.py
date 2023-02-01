from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/$", consumers.LightConsumer.as_asgi()),
    re_path(r'ws/TelegramUsers/$', consumers.UserConsumer.as_asgi()),
]