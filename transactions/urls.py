from django.urls import path
from . import views

urlpatterns = [
    path('points_transfer', views.money_transfer, name='points_transfer'),
    path('list_transactions', views.list_transactions, name='list_transactions'),
    path('payment_request', views.payment_request, name='payment_request'),
    path('payment_req_history', views.view_payment_requests, name='view_payment_requests'),
    path('payment_request/accept/<int:request_id>/', views.accept_payment, name='accept_payment'),
    path('payment_request/reject/<int:request_id>/', views.reject_payment, name='reject_payment'),
    path('notifications/read/<int:notification_id>/', views.mark_as_read, name='mark_notification_read'),

]
