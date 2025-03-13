import pytest
from django.core.exceptions import ValidationError

from quotes.models import CryptoQuote

@pytest.mark.django_db
def test_crypto_quote_creation():
    quote = CryptoQuote.objects.create(crypto_pair="BTCUSDT", price=50000.00)

    assert quote.crypto_pair == "BTCUSDT"
    assert quote.price == 50000.00
    assert quote.created_at is not None

@pytest.mark.django_db
def test_crypto_quote_validation():
    # Объект с некорректными данными
    with pytest.raises(ValidationError):
        quote = CryptoQuote(crypto_pair="INVALID", price=-100)
        quote.full_clean()  # Вызов валидации