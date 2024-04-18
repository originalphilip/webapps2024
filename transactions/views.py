from django.db import transaction, OperationalError
from django.db.models import F
from django.shortcuts import render, redirect, get_object_or_404
from . import models
from transactions.forms import MoneyTransferForm, PaymentRequestForm
from .models import Points
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Transaction, PaymentRequest
from django.contrib.auth.models import User


@login_required()
@transaction.atomic()
def money_transfer(request):
    if request.method == 'POST':
        form = MoneyTransferForm(request.POST)

        if form.is_valid():

            src_username = form.cleaned_data["enter_your_username"]
            dst_username = form.cleaned_data["enter_destination_username"]
            points_to_transfer = form.cleaned_data["enter_points_to_transfer"]

            src_user = User.objects.get(username=src_username)
            dst_user = User.objects.get(username=dst_username)

            src_points = Points.objects.select_for_update().get(user=src_user)
            dst_points = Points.objects.select_for_update().get(user=dst_user)

            if src_points.amount >= points_to_transfer:
                src_points.amount = src_points.amount - points_to_transfer
                src_points.save()

                dst_points.amount = dst_points.amount + points_to_transfer
                dst_points.save()

                Transaction.objects.create(
                    sender=src_user,
                    receiver=dst_user,
                    amount=points_to_transfer,
                    status='completed'  # Assuming you have such a field
                )

                transaction.on_commit(lambda: messages.success(request, "Points transferred successfully."))
                return redirect('list_transactions')
            else:
                messages.error(request, "Insufficient points for transfer.")
    else:
        form = MoneyTransferForm()

    return render(request, "transactions/moneytransfer.html", {"form": form})


@login_required()
def payment_request(request):
    if request.method == 'POST':
        form = PaymentRequestForm(request.POST)
        if form.is_valid():
            dst_username = form.cleaned_data['enter_destination_username']
            amount_requested = form.cleaned_data['enter_amount_to_request']
            message = form.cleaned_data['message']

            try:
                dst_user = User.objects.get(username=dst_username)
                PaymentRequest.objects.create(
                    sender=request.user,
                    enter_destination_username=dst_user,
                    enter_amount_to_request=amount_requested,
                    message=message,
                )
                messages.success(request,"Payment Request sent")
                return redirect('list_transactions')
            except User.DoesNotExist:
                messages.error(request, "Cant find user")
        else:
            messages.error(request,"Invalid information entered")
    else:
        form = PaymentRequestForm()

    return render(request, "transactions/request_payments.html", {"form": form})


@login_required
def list_transactions(request):
    transactions = Transaction.objects.filter(sender=request.user) | Transaction.objects.filter(receiver=request.user)
    transactions = transactions.order_by('-timestamp')#order by most recent transaction
    return render(request, "transactions/transaction_history.html", {'transactions': transactions})


@login_required()
def view_payment_requests(request):
    received_requests = PaymentRequest.objects.filter(enter_destination_username=request.user).order_by('-id')
    return render(request, "transactions/payment_req_history.html", {'received_requests': received_requests})


@login_required()
def accept_payment(request, request_id):
    payment_request = get_object_or_404(PaymentRequest, id=request_id, enter_destination_username=request.user)
    payment_request.status = 'accepted'
    payment_request.save()
    messages.success(request, "Payment request accepted.")
    return redirect('view_payment_requests')


@login_required()
def reject_payment(request, request_id):
    payment_request = get_object_or_404(PaymentRequest, id=request_id, enter_destination_username=request.user)
    payment_request.status = 'rejected'
    payment_request.save()
    messages.success(request, "Payment request rejected.")
    return redirect('view_payment_requests')