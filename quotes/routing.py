"""Модуль URL-маршрут для WebSocket-соединений"""

from django.urls import path

from .consumers import CryptoQuoteConsumer

websocket_urlpatterns = [
    path("ws/crypto/", CryptoQuoteConsumer.as_asgi())
]