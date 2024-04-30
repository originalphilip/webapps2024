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
from .utils import get_currency_conversion
from register.models import Profile



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

            src_currency = src_user.profile.currency
            dst_currency = dst_user.profile.currency

            conversion_result = get_currency_conversion(src_currency, dst_currency, points_to_transfer)
            if 'converted_amount' in conversion_result:
                converted_amount = conversion_result['converted_amount']
            else:
                messages.error(request, "Failed to convert currency.")
                return render(request, "transactions/moneytransfer.html", {"form": form})

            print(type(src_points.amount), src_points.amount)
            print(type(converted_amount), converted_amount)

            if src_points.amount >= converted_amount:
                src_points.amount -= converted_amount
                src_points.save()

                dst_points.amount += converted_amount
                dst_points.save()

                Transaction.objects.create(
                    sender=src_user,
                    receiver=dst_user,
                    amount=converted_amount,
                    currency=dst_currency,
                    status='completed'
                )

                messages.success(request, "Money transferred successfully.")
                return redirect('list_transactions')
            else:
                messages.error(request, "Insufficient money for transfer.")
    else:
        form = MoneyTransferForm()

    return render(request, "transactions/moneytransfer.html", {"form": form})


@login_required()
def payment_request(request):
    if request.method == 'POST':
        form = PaymentRequestForm(request.POST)
    else:
        # Initialize the form with the current user set as the sender
        initial_data = {'sender': request.user.username}  # assuming the form needs a username
        form = PaymentRequestForm(initial=initial_data)
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
                status='pending'
            )
            messages.success(request,"Payment Request sent")
            return redirect('list_transactions')
        except User.DoesNotExist:
            messages.error(request, "Cant find user")
        pass
    else:
        messages.error(request,"Invalid information entered")
    return render(request, "transactions/request_payments.html", {"form": form})


@login_required
def list_transactions(request):
    transactions = Transaction.objects.filter(sender=request.user) | Transaction.objects.filter(receiver=request.user)
    transactions = transactions.order_by('-timestamp')
    user_profile = Profile.objects.get(user=request.user)
    currency = user_profile.currency

    converted_transactions = []
    for transaction in transactions:
        conversion_result = get_currency_conversion(transaction.currency, currency, transaction.amount)
        if 'converted_amount' in conversion_result:
            amount = conversion_result['converted_amount']
        else:
            amount = transaction.amount
            currency = transaction.currency

        converted_transactions.append({
            'sender': transaction.sender.username,
            'receiver': transaction.receiver.username,
            'amount': amount,
            'currency': currency,
            'timestamp': transaction.timestamp,
            'status': transaction.status
        })

    return render(request, "transactions/transaction_history.html", {
        'transactions': converted_transactions,
        'user_currency': currency
    })


@login_required()
def view_payment_requests(request):
    received_requests = PaymentRequest.objects.filter(enter_destination_username=request.user).order_by('-id')
    return render(request, "transactions/payment_req_history.html", {'received_requests': received_requests})


@login_required()
def accept_payment(request, request_id):
    payment_request = PaymentRequest.objects.get(id=request_id)
    if payment_request.status == 'pending':

        # do transaction
        src_user = payment_request.sender
        dst_user = User.objects.get(username=payment_request.enter_destination_username)

        requester_money = Points.objects.select_for_update().get(user=src_user)
        responder_money = Points.objects.select_for_update().get(user=dst_user)

        if responder_money.amount >= payment_request.enter_amount_to_request:
            # perform transaction
            responder_money.amount -= payment_request.enter_amount_to_request
            requester_money.amount += payment_request.enter_amount_to_request
            responder_money.save()
            requester_money.save()

            # Record the transaction
            Transaction.objects.create(
                sender=src_user,
                receiver=dst_user,
                amount=payment_request.enter_amount_to_request,
                status='completed'
            )
            # update payment status
            payment_request.status = 'accepted'
            payment_request.save()

            messages.success(request, "Payment accepted.")
        else:
            payment_request.status = 'failed'
            payment_request.save()
            messages.error(request, "Transaction failed due to insufficient funds.")
    else:
        messages.error(request, "Invalid payment request status.")
    return redirect('view_payment_requests')


@login_required()
def reject_payment(request, request_id):
    payment_request = get_object_or_404(PaymentRequest, id=request_id, enter_destination_username=request.user)
    payment_request.status = 'rejected'
    payment_request.save()
    messages.success(request, "Payment request rejected.")
    return redirect('view_payment_requests')