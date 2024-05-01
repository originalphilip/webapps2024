def convert_currency(currency1, currency2, amount):
    exchange_rates = {
        'USD': {'EUR': 0.93, 'GBP': 0.82, 'USD': 1.0},
        'EUR': {'USD': 1.08, 'GBP': 0.88, 'EUR': 1.0},
        'GBP': {'USD': 1.22, 'EUR': 1.14, 'GBP': 1.0}
    }
    try:
        rate = exchange_rates[currency1][currency2]
        converted_amount = amount * rate
        return round(converted_amount, 2)
    except KeyError:
        raise ValueError(f"No conversion rate for {currency1} to {currency2}.")
    except TypeError:
        raise ValueError("Invalid amount provided; must be a number.")