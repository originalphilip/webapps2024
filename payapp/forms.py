# from django import forms
# from django.contrib.auth.models import User
# from django.core.exceptions import ValidationError
#
#
# def validate_user_exists(value):
#     if not User.objects.filter(username=value).exists():
#         raise ValidationError(f"User {value} does not exist.")
#
#
# class MakePaymentForm(forms.Form):
#     receiver = forms.CharField(label="Receiver Username:", max_length=15, validators=[validate_user_exists])
#     amount = forms.DecimalField(label="Amount:", max_digits=10, decimal_places=2)
#
#
# class RequestPaymentForm(forms.Form):
#     requestee = forms.CharField(label="Requestee Username:", max_length=150, validators=[validate_user_exists])
#     amount = forms.DecimalField(label="Amount:", max_digits=10, decimal_places=2)