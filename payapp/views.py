from django.shortcuts import render, redirect
from transactions.models import Points
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    account = Points.objects.get(user=request.user)
    return render(request, 'payapp/home.html', {'account': account})
