
def convert_currency(currency1, currency2, amount):
    exchange_rates = {
        'USD': {'EUR': 0.93, 'GBP': 0.82, 'USD': 1.0},
        'EUR': {'USD': 1.08, 'GBP': 0.88, 'EUR': 1.0},
        'GBP': {'USD': 1.22, 'EUR': 1.14, 'GBP': 1.0}
    }

    if currency1 not in exchange_rates or currency2 not in exchange_rates[currency1]:
        return None

    rate = exchange_rates[currency1][currency2]
    return  amount * rate