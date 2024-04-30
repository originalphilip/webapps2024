from django.shortcuts import render, redirect
from transactions.models import Points
from transactions.models import Transaction
from django.contrib.auth.decorators import login_required
from register.models import Profile


@login_required
def home(request):
    account = Profile.objects.get(user=request.user)
    context = {
        'account': account
    }
    return render(request, 'payapp/home.html', context)
