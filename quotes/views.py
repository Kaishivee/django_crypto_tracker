from rest_framework import viewsets
from .models import CryptoQuote
from .serializers import CryptoQuoteSerializer
from django_filters import rest_framework as filters

# фильтр
class CryptoQuoteFilter(filters.FilterSet):
    crypto_pair = filters.CharFilter(field_name="crypto_pair", lookup_expr="iexact")

    class Meta:
        model = CryptoQuote
        fields = ["crypto_pair"]

class CryptoQuoteViewSet(viewsets.ModelViewSet):
    queryset = CryptoQuote.objects.all()
    serializer_class = CryptoQuoteSerializer
    filterset_class = CryptoQuoteFilter