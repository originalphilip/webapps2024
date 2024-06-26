from django.contrib.auth.models import User
from django.db import models


class Points(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(default=1000, max_digits=10, decimal_places=2)

    def __str__(self):
        details = ''
        details += f'Username     : {self.user.username}\n'
        details += f'Points       : {self.amount}\n'
        return details


class PointsTransfer(models.Model):
    enter_your_username = models.CharField(max_length=50)
    enter_destination_username = models.CharField(max_length=50)
    enter_points_to_transfer = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        details = ''
        details += f'Your username            : {self.enter_your_username}\n'
        details += f'Destination username     : {self.enter_destination_username}\n'
        details += f'Points To Transfer         : {self.enter_points_to_transfer}\n'
        return details


class Transaction(models.Model):
    sender = models.ForeignKey(User, related_name='sent_transactions', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_transactions', on_delete=models.CASCADE)
    original_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    original_currency = models.CharField(max_length=3, null=True)
    converted_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    converted_currency = models.CharField(max_length=3, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, default='completed')

    def __str__(self):
        return f'{self.sender.username} -> {self.receiver.username}: {self.original_amount} {self.original_currency} on {self.timestamp.strftime("%Y-%m-%d %H:%M:%S")}'


class PaymentRequest(models.Model):
    sender = models.ForeignKey(User, related_name='sent_payment_requests', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_payment_requests', on_delete=models.CASCADE, null=True)#change to null=false when fields are updated
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, null=True)#change to null=false when fields are updated
    message = models.TextField(default='', blank=True)
    status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending')

    def __str__(self):
        return f"{self.amount} {self.currency} from {self.sender.username} to {self.receiver.username} status {self.status}"


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Notification for {self.user.username} - Read: {self.read}'
