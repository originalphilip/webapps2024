from django.urls import path
from . import views

urlpatterns = [
    path('points_transfer', views.money_transfer, name='points_transfer'),
    path('list_transactions', views.list_transactions, name='list_transactions'),
]
