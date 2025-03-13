import pytest
import json
from unittest.mock import patch, AsyncMock

from quotes.binance_client import process_message


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_process_message():
    # Мок данных от Binance
    message = json.dumps({
        "s": "BTCUSDT",
        "p": "50000.00",
    })

    # Мок модели и channel_layer
    with patch("quotes.models.CryptoQuote.objects.create") as mock_create, \
         patch("quotes.binance_client.get_channel_layer") as mock_channel_layer:

        mock_channel_layer.return_value = AsyncMock()
        await process_message(message)

        # Проверка, что данные сохраняются в базу
        mock_create.assert_called_once_with(crypto_pair="BTCUSDT", price=50000.00)

        # Проверка, что сообщение отправляется в группу WebSocket
        mock_channel_layer.return_value.group_send.assert_called_once()