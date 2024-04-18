from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Points)
admin.site.register(PointsTransfer)
admin.site.register(Transaction)
#admin.site.register(MoneyRequest)