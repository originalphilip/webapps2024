from django.urls import path
from . import views

urlpatterns = [
    path('points_transfer', views.money_transfer, name='points_transfer'),
    path('list_transactions', views.list_transactions, name='list_transactions'),
    path('payment/request/', views.create_payment_request, name='create_payment_request'),
    path('payment/view/', views.view_payment_requests, name='view_payment_requests'),
    path('payment/accept/<int:payment_request_id>/', views.accept_payment_request, name='accept_payment_request'),
    path('payment/reject/<int:request_id>/', views.reject_payment_request, name='reject_payment_request'),
    path('notifications/read/<int:notification_id>/', views.mark_as_read, name='mark_notification_read'),

]
