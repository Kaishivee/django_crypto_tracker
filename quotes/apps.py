from django.apps import AppConfig
import threading
import asyncio
import os

def start_websocket():
    """Запуск WebSocket-клиента в отдельном потоке"""
    from .binance_client import start_binance_websocket

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(start_binance_websocket())

class QuotesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "quotes"

    def ready(self):
        """Запускает WebSocket после миграций в отдельном потоке"""
        if os.environ.get("RUN_MAIN") == "true":
            thread = threading.Thread(target=start_websocket, daemon=True)
            thread.start()
