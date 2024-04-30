from django.db import models


# Create your models here.
class CurrencyConverter(models.Model):
    currency1 = models.CharField(max_length=3)
    currency2 = models.CharField(max_length=3)
    rate = models.DecimalField(max_digits=13, decimal_places=6)

    def __str__(self):
        return f"{self.currency1}/{self.currency2}: {self.rate}"
