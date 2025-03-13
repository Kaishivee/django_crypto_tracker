"""
Модуль WebSocket-консюмеров для обработки обновлений цен криптовалют
"""

import json
from channels.generic.websocket import AsyncWebsocketConsumer


class CryptoQuoteConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """Обрабатывает подключение WebSocket-клиента и добавляет его в группу 'updates'"""
        await self.accept()
        await self.channel_layer.group_add("updates", self.channel_name)

    async def disconnect(self, close_code):
        """Обрабатывает отключение WebSocket-клиента и удаляет его из группы 'updates'"""
        await self.channel_layer.group_discard("updates", self.channel_name)

    async def send_update(self, event):
        """Отправляет обновления цен клиенту через WebSocket"""
        await self.send(text_data=json.dumps({
            "crypto_pair": event["crypto_pair"],
            "price": "{:.2f}".format(float(event["price"])),
            "created_at": event["created_at"],
        }))
