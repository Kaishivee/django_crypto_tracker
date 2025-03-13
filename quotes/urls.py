from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CryptoQuoteViewSet,websocket_client

router = DefaultRouter()
router.register(r'crypto-quotes', CryptoQuoteViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path("ws-client/", websocket_client, name="websocket_client"),

]