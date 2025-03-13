import pytest

from quotes.serializers import CryptoQuoteSerializer
from quotes.models import CryptoQuote

@pytest.mark.django_db
def test_crypto_quote_serializer():
    # Создаем объект
    quote = CryptoQuote.objects.create(crypto_pair="BTCUSDT", price=50000.00)

    # Сериализуем объект
    serializer = CryptoQuoteSerializer(quote)
    data = serializer.data

    # Проверяем сериализованные данные
    assert data["crypto_pair"] == "BTCUSDT"
    assert data["price"] == "50000.00"
    assert isinstance(data["created_at"], str)

@pytest.mark.django_db
def test_crypto_quote_deserializer():
    # Данные для десериализации
    data = {
        "crypto_pair": "ETHUSDT",
        "price": "3000.00",
    }

    # Десериализуем данные
    serializer = CryptoQuoteSerializer(data=data)
    assert serializer.is_valid()

    # Создаем объект
    quote = serializer.save()
    assert quote.crypto_pair == "ETHUSDT"
    assert quote.price == 3000.00