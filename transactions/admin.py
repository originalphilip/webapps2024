from django.contrib import admin
from .models import *
# Register your models here.


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'original_amount', 'original_currency', 'converted_amount',
                    'converted_currency', 'timestamp', 'status')
    search_fields = ('sender__username', 'receiver__username')
    list_filter = ('status', 'original_currency', 'converted_currency')


admin.site.register(Transaction, TransactionAdmin)


class PaymentRequestAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'amount', 'currency', 'status')
    search_fields = ('sender__username', 'receiver__username')
    list_filter = ('status', 'currency')


class PointsAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount')
    search_fields = ('user__username',)


admin.site.register(PaymentRequest, PaymentRequestAdmin)
admin.site.register(Points, PointsAdmin)
