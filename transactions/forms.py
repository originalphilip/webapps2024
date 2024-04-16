from django import forms
from . import models


class MoneyTransferForm(forms.ModelForm):
    class Meta:
        model = models.PointsTransfer
        fields = ["enter_your_username", "enter_destination_username", "enter_points_to_transfer"]
