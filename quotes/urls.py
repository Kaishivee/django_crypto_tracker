from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CryptoQuoteViewSet

router = DefaultRouter()
router.register(r'crypto-quotes', CryptoQuoteViewSet)

urlpatterns = [
    path('', include(router.urls)),
]