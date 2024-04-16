from django.urls import path
from . import views

urlpatterns = [
    # path('make_payment/', views.make_payment, name='make_payment'),
    # path('request_payment/', views.request_payment, name='request_payment'),
    #path('', views.list_transactions, name='payapp'),
    path('', views.home, name="home"),
    path('home/', views.home, name="home"),
    #path('payapp/', views.)
]
