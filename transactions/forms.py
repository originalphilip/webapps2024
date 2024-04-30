from django import forms
from django.core.exceptions import ValidationError
from . import models


class MoneyTransferForm(forms.ModelForm):
    class Meta:
        model = models.PointsTransfer
        fields = ["enter_your_username", "enter_destination_username", "enter_points_to_transfer"]


class PaymentRequestForm(forms.ModelForm):
    class Meta:
        model = models.PaymentRequest
        fields = ["enter_destination_username", "enter_amount_to_request", "message"]

    def clean(self):
        cleaned_data = super().clean()
        sender_username = self.initial.get('sender')  # safer access
        enter_destination_username = cleaned_data.get('enter_destination_username')

        if sender_username and enter_destination_username == sender_username:
            raise forms.ValidationError("You cannot send a request to yourself.")

        return cleaned_data
