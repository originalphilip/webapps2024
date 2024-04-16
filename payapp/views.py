from django.shortcuts import render, redirect
from transactions.models import Points


def home(request):
    account = Points.objects.get(user=request.user)
    return render(request, 'payapp/home.html', {'account': account})
