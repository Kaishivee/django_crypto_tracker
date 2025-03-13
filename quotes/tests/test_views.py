import pytest
from rest_framework.test import APIClient
from django.urls import reverse

from quotes.models import CryptoQuote

@pytest.mark.django_db
def test_crypto_quotes_list():
    # Очищаем базу данных перед тестом
    CryptoQuote.objects.all().delete()

    CryptoQuote.objects.create(crypto_pair="BTCUSDT", price=50000.00)
    CryptoQuote.objects.create(crypto_pair="ETHUSDT", price=3000.00)

    # Запрос к API
    client = APIClient()
    url = reverse("cryptoquote-list")
    response = client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 2
    assert response.data[0]["crypto_pair"] == "BTCUSDT"
    assert response.data[1]["crypto_pair"] == "ETHUSDT"

@pytest.mark.django_db
def test_crypto_quotes_filter_by_pair():
    CryptoQuote.objects.all().delete()

    CryptoQuote.objects.create(crypto_pair="BTCUSDT", price=50000.00)
    CryptoQuote.objects.create(crypto_pair="ETHUSDT", price=3000.00)

    # Запрос к API с фильтром
    client = APIClient()
    url = reverse("cryptoquote-list") + "?crypto_pair=BTCUSDT"
    response = client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["crypto_pair"] == "BTCUSDT"