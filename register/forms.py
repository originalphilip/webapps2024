from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from transactions.models import Points
from .models import Profile
from .utils import get_currency_conversion


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
        chosen_currency = self.cleaned_data['currency']
        base_amount = 1000
        if chosen_currency != 'GBP':
            conversion_result = get_currency_conversion('GBP', chosen_currency, base_amount)
            if conversion_result and 'converted_amount' in conversion_result:
                amount = conversion_result['converted_amount']
            else:
                amount = base_amount
        else:
            amount = base_amount
        Points.objects.create(user=user, amount=amount)
        user.save()
        user_profile = Profile(user=user, currency=chosen_currency)
        user_profile.save()
        return user
