"""
Модуль для подключения к WebSocket API Binance и обработки сообщений.
"""
from dotenv import load_dotenv
import json
import os

import websockets
from channels.layers import get_channel_layer
from asgiref.sync import sync_to_async
import time

load_dotenv()

BINANCE_WEBSOCKET_URL = os.getenv("BINANCE_WEBSOCKET_URL")


last_update_time = 0  # Время последнего обновления


async def start_binance_websocket():
    """Устанавливает соединение с WebSocket API Binance и получает обновления в реальном времени."""
    url = BINANCE_WEBSOCKET_URL
    async with websockets.connect(url) as ws:
        while True:
            try:
                message = await ws.recv()
                await process_message(message)
            except websockets.ConnectionClosed:
                break
            except Exception as e:
                print(f"WebSocket error: {e}")
                break


async def process_message(message):
    """
    Обрабатывает полученное сообщение с Binance.

    Извлекает цену и торговую пару, сохраняет данные в базу каждую минуту.
    Отправляет обновленные данные в WebSocket-группу "updates".
    """
    global last_update_time

    from .models import CryptoQuote  # Импорт модели внутри функции для избежания циклического импорта

    data = json.loads(message)
    crypto_pair = data.get('s')
    price = data.get('p')

    if crypto_pair and price:
        current_time = time.time()
        if current_time - last_update_time >= 60:  # Проверка, прошло ли 60 секунд с последнего обновления
            quote = await sync_to_async(CryptoQuote.objects.create)(
                crypto_pair=crypto_pair, price=float(price)
            )

            channel_layer = get_channel_layer()
            await channel_layer.group_send(
                "updates",
                {
                    "type": "send_update",
                    "crypto_pair": quote.crypto_pair,
                    "price": str(quote.price),
                    "created_at": quote.created_at.isoformat(),
                }
            )

            last_update_time = current_time
            print(f"Received update for {crypto_pair}: {price}")
