from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CurrencyConverter
from .serializers import CurrencyConverterSerializer
from .utils import convert_currency

# Create your views here.


class CurrencyConverterView(APIView):
    serializer = CurrencyConverterSerializer()

    def get(self, request, currency1, currency2, amount):
        try:
            amount = float(amount)
            converted_amount = convert_currency(currency1.upper(), currency2.upper(), amount)
            if converted_amount is None:
                return Response({"error": "Invalid currency or conversion error"}, status=400)
            return Response({"converted_amount": converted_amount})
        except ValueError:
            return Response({"error": "Invalid amount provided"}, status=400)
