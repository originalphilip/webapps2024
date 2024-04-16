from django.contrib.auth.models import User
from django.db import models


class Points(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField(default=1000)

    def __str__(self):
        details = ''
        details += f'Username     : {self.user.username}\n'
        details += f'Points       : {self.amount}\n'
        return details


class PointsTransfer(models.Model):
    enter_your_username = models.CharField(max_length=50)
    enter_destination_username = models.CharField(max_length=50)
    enter_points_to_transfer = models.IntegerField()

    def __str__(self):
        details = ''
        details += f'Your username            : {self.enter_your_username}\n'
        details += f'Destination username     : {self.enter_destination_username}\n'
        details += f'Points To Transfer         : {self.enter_points_to_transfer}\n'
        return details


class Transaction(models.Model):
    sender = models.ForeignKey(User, related_name='sent_transactions', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_transactions', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, default='completed')

    def __str__(self):
        return f'{self.sender} -> {self.receiver}: ${self.amount} on {self.timestamp.strftime("%Y-%m-%d %H:%M:%S")}'
