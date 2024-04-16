# from django.db import models
# from django.contrib.auth.models import User
#
#
# class PaymentRequest(models.Model):
#     requester = models.ForeignKey(User, related_name='payment_requests_made', on_delete=models.CASCADE)
#     requestee = models.ForeignKey(User, related_name='payment_requests_recieved', on_delete=models.CASCADE)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     timestamp = models.DateTimeField(auto_now=True)
#     status = models.CharField(max_length=100, choices=(('pending', 'Pending'), ('paid', 'Paid')), default='pending')
#
#     def __str__(self):
#         return f'{self.requester} requests ${self.amount} from {self.requestee} - Status: {self.status}'