from django.shortcuts import render, redirect
from transactions.models import Points
from transactions.models import Transaction
from django.contrib.auth.decorators import login_required
from register.models import Profile


@login_required
def home(request):
    profile = Profile.objects.get(user=request.user)
    try:
        points = Points.objects.get(user=request.user)
    except Points.DoesNotExist:
        points = None

    context = {
        'account': profile,
        'points': points,
        'is_admin': request.user.is_staff,
    }
    return render(request, 'payapp/home.html', context)
