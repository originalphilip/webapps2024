from rest_framework import serializers
from .models import CurrencyConverter


class CurrencyConverterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrencyConverter
        fields = ('currency1', 'currency2', 'rate')
