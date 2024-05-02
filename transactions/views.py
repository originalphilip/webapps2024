from django.db import transaction, OperationalError
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from transactions.forms import MoneyTransferForm, PaymentRequestForm
from .models import Points, Notification, Transaction, PaymentRequest
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .utils import get_currency_conversion, transfer_money
from register.models import Profile
from decimal import Decimal

@login_required()
@transaction.atomic()
def money_transfer(request):
    if request.method == 'POST':
        form = MoneyTransferForm(request.POST)
        if form.is_valid():
            dst_username = form.cleaned_data["enter_destination_username"]
            amount = form.cleaned_data["enter_points_to_transfer"]
            src_user = request.user
            dst_user = User.objects.get(username=dst_username)

            success, message = transfer_money(src_user, dst_user, amount)
            messages.info(request, message)
            if success:
                return redirect('list_transactions')
            else:
                return render(request, "transactions/moneytransfer.html", {"form": form})
    else:
        form = MoneyTransferForm()
        return render(request, "transactions/moneytransfer.html", {"form": form})


@login_required
def list_transactions(request):
    transactions = Transaction.objects.filter(sender=request.user) | Transaction.objects.filter(receiver=request.user)
    transactions = transactions.order_by('-timestamp')
    user_profile = Profile.objects.get(user=request.user)
    user_currency = user_profile.currency

    converted_transactions = []
    for transaction in transactions:
        if request.user == transaction.sender:
            amount = transaction.original_amount
            transaction_currency = transaction.original_currency
        else:
            amount = transaction.converted_amount
            transaction_currency = transaction.converted_currency

        converted_transactions.append({
            'sender': transaction.sender.username,
            'receiver': transaction.receiver.username,
            'amount': amount,
            'currency': transaction_currency,
            'timestamp': transaction.timestamp,
            'status': transaction.status
        })

    return render(request, "transactions/transaction_history.html", {
        'transactions': converted_transactions,
        'user_currency': user_currency
    })

@login_required
def create_payment_request(request):
    if request.method == 'POST':
        form = PaymentRequestForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['receiver']
            amount = form.cleaned_data['amount']
            message = form.cleaned_data['message']

            try:
                receiver = User.objects.get(username=username)
            except User.DoesNotExist:
                messages.error(request, "User not found.")
                return render(request, 'transactions/create_payment_request.html', {'form': form})

            payment_request = PaymentRequest(
                sender=request.user,
                receiver=receiver,
                amount=amount,
                currency=request.user.profile.currency,
                message=message
            )
            payment_request.save()
            messages.success(request, "Payment request created successfully.")
            return redirect('view_payment_requests')
        else:
            messages.error(request, "Invalid data entered.")
    else:
        form = PaymentRequestForm()

    return render(request, 'transactions/create_payment_request.html', {'form': form})

@login_required
def view_payment_requests(request):
    payment_requests = PaymentRequest.objects.filter(receiver=request.user, status='pending')
    return render(request, 'transactions/view_payment_requests.html', {'payment_requests': payment_requests})

@login_required
def accept_payment_request(request, payment_request_id):
    payment_request = get_object_or_404(PaymentRequest, id=payment_request_id, receiver=request.user)
    if payment_request.status == 'pending':
        success, message = transfer_money(payment_request.sender, request.user, payment_request.amount)

        if success:
            payment_request.status = 'accepted'
            payment_request.save()
            messages.success(request, "Payment request accepted and money transferred.")
        else:
            messages.error(request, message)

        return redirect('list_transactions')
    else:
        messages.error(request, "This payment request has already been processed.")
        return redirect('list_transactions')

@login_required
def reject_payment_request(request, request_id):
    payment_request = get_object_or_404(PaymentRequest, id=request_id, receiver=request.user)
    payment_request.status = 'rejected'
    payment_request.save()
    return redirect('view_payment_requests')

def notifications(request):
    user_notifications = Notification.objects.filter(user=request.user, read=False)
    return render(request, 'notifications.html', {'notifications': user_notifications})

@require_POST
def mark_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.read = True
    notification.save()
    return redirect(request.META.get('HTTP_REFERER', 'home'))
