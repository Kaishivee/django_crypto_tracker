import pytest
from asgiref.sync import sync_to_async
from channels.layers import get_channel_layer
from channels.testing import WebsocketCommunicator

from quotes.consumers import CryptoQuoteConsumer
from quotes.models import CryptoQuote

@pytest.mark.django_db
@pytest.mark.asyncio
async def test_crypto_quote_consumer_connect_disconnect():
    # Подключение к WebSocket
    communicator = WebsocketCommunicator(CryptoQuoteConsumer.as_asgi(), "/ws/crypto/")
    connected, _ = await communicator.connect()
    assert connected

    # Отключение
    await communicator.disconnect()

@pytest.mark.django_db
@pytest.mark.asyncio
async def test_crypto_quote_consumer_receive_update():
    quote = await sync_to_async(CryptoQuote.objects.create)(crypto_pair="BTCUSDT", price=50000.00)

    communicator = WebsocketCommunicator(CryptoQuoteConsumer.as_asgi(), "/ws/crypto/")
    connected, _ = await communicator.connect()
    assert connected

    # Мок channel_layer
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

    # Проверяем получение сообщения
    response = await communicator.receive_json_from(timeout=5)
    assert response == {
        "crypto_pair": "BTCUSDT",
        "price": "50000.00",
        "created_at": quote.created_at.isoformat(),
    }

    await communicator.disconnect()