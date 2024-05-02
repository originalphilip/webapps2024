from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from . import models
from .models import PaymentRequest


class MoneyTransferForm(forms.Form):
    enter_destination_username = forms.CharField(label='Destination Username', max_length=150)
    enter_points_to_transfer = forms.DecimalField(label='Amount to Transfer', max_digits=10, decimal_places=2)

    def clean_enter_destination_username(self):
        username = self.cleaned_data['enter_destination_username']
        if not User.objects.filter(username=username).exists():
            raise ValidationError("The entered username does not exist.")
        return username

    def clean_enter_points_to_transfer(self):
        points = self.cleaned_data['enter_points_to_transfer']
        if points <= 0:
            raise ValidationError("Enter a valid amount to transfer.")
        return points


class PaymentRequestForm(forms.ModelForm):
    receiver = forms.CharField(required=True)

    class Meta:
        model = PaymentRequest
        fields = ['receiver', 'amount', 'message']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(PaymentRequestForm, self).__init__(*args, **kwargs)

    def clean_receiver(self):
        username = self.cleaned_data.get('receiver')
        if username == self.user.username:
            raise ValidationError("You cannot send a payment request to yourself.")
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise ValidationError("The entered username does not exist.")
        return user
