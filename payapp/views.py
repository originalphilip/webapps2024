from django.shortcuts import render, redirect
from transactions.models import Points
from transactions.models import Transaction
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    transactions = Transaction.objects.filter(sender=request.user) | Transaction.objects.filter(receiver=request.user)
    transactions = transactions.order_by('-timestamp')[:10]  # Only get the most recent 10 transactions
    account = Points.objects.get(user=request.user)
    context = {
        'transactions': transactions,
        'account': account
    }
    return render(request, 'payapp/home.html', context)
