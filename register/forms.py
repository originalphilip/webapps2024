from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from transactions.models import Points


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    currency = forms.ChoiceField(choices=(('GBP', 'British Pound'), ('USD', 'US Dollar'), ('EUR', 'Euro')))

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name",  "password1", "password2", "currency")

    def save(self, *args, **kwargs):
        user = super(RegisterForm, self).save(*args, **kwargs)
        Points.objects.create(name=user)
        return user

