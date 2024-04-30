from django.urls import path
from .views import CurrencyConverterView

urlpatterns = [
    path('<str:currency1>/<str:currency2>/<amount>/', CurrencyConverterView.as_view(), name='conversion'),
]
# baseURL/conversion/{currency1}/{currency2}/{amount_of_currency1}
