from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

from django.db import models

class CryptoQuote(models.Model):
    crypto_pair = models.CharField(max_length=10)
    price = models.DecimalField(
        max_digits=20,
        decimal_places=10,
        validators=[MinValueValidator(0)]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.crypto_pair} - {self.price}"

    def clean(self):
        # Кастомная валидация для crypto_pair :)
        if len(self.crypto_pair) != 7:
            raise ValidationError({"crypto_pair": "Длина crypto_pair должна быть 7 символов."})
        if not self.crypto_pair.isupper():
            raise ValidationError({"crypto_pair": "crypto_pair должен быть в верхнем регистре."})