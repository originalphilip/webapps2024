from django.db import transaction, OperationalError
from django.db.models import F
from django.shortcuts import render, redirect
from . import models
from transactions.forms import MoneyTransferForm
from .models import Points
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Transaction
from django.contrib.auth.models import User


@transaction.atomic()
def money_transfer(request):
    if request.method == 'POST':
        form = MoneyTransferForm(request.POST)

        if form.is_valid():

            src_username = form.cleaned_data["enter_your_username"]
            dst_username = form.cleaned_data["enter_destination_username"]
            points_to_transfer = form.cleaned_data["enter_points_to_transfer"]

            src_points = Points.objects.select_for_update().get(name__username=src_username)
            dst_points = Points.objects.select_for_update().get(name__username=dst_username)

            if src_points.amount >= points_to_transfer:
                src_points.amount = src_points.amount - points_to_transfer
                src_points.save()

                dst_points.amount = dst_points.amount + points_to_transfer
                dst_points.save()

                Transaction.objects.create(
                    sender=User.objects.get(username=src_username),
                    receiver=User.objects.get(username=dst_username),
                    amount=points_to_transfer,
                    status='completed'  # Assuming you have such a field
                )

                transaction.on_commit(lambda: messages.success(request, "Points transferred successfully."))
                return redirect('transactions:list_transactions')
            else:
                messages.error(request, "Insufficient points for transfer.")
    else:
        form = MoneyTransferForm()

    return render(request, "transactions/moneytransfer.html", {"form": form})


@login_required
def list_transactions(request):
    transactions = Transaction.objects.filter(sender=request.user) | Transaction.objects.filter(receiver=request.user)
    return render(request, "transactions/transaction_history.html", {'transactions': transactions})

