from rest_framework import serializers
from .models import CryptoQuote

class CryptoQuoteSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(max_digits=20, decimal_places=2, coerce_to_string=True)

    class Meta:
        model = CryptoQuote
        fields = ['crypto_pair', 'price', 'created_at']