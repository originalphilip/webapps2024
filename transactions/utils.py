import requests
from django.db.models import F
from .models import Points, Transaction


def get_currency_conversion(base_currency, target_currency, amount):
    url = f"http://localhost:8000/webapps2024/conversion/{base_currency}/{target_currency}/{amount}"

    try:
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            return {"error": f"Failed to convert currency. Status Code: {response.status_code}", "details": response.text}
    except Exception as e:
        return {"error": "An error occurred while making the request.", "details": str(e)}


def transfer_money(src_user, dst_user, amount):
    src_points = Points.objects.select_for_update().get(user=src_user)
    dst_points = Points.objects.select_for_update().get(user=dst_user)

    src_currency = src_user.profile.currency
    dst_currency = dst_user.profile.currency

    if src_currency == dst_currency:
        converted_amount = amount
    else:
        conversion_result = get_currency_conversion(src_currency, dst_currency, amount)
        if 'converted_amount' in conversion_result:
            converted_amount = conversion_result['converted_amount']
        else:
            return False, "Failed to convert currency."

    if src_points.amount >= converted_amount:
        src_points.amount = F('amount') - amount
        src_points.save(update_fields=['amount'])

        dst_points.amount = F('amount') + converted_amount
        dst_points.save(update_fields=['amount'])

        Transaction.objects.create(
            sender=src_user,
            receiver=dst_user,
            original_amount=amount,
            original_currency=src_currency,
            converted_amount=converted_amount,
            converted_currency=dst_currency,
            status='completed'
        )
        return True, "Money transferred successfully."
    else:
        return False, "Insufficient funds."
