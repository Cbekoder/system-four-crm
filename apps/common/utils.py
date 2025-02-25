from django.core.cache import cache


exchange_rates = {
    'USD': 1.0,
    # 'UZS': cache.get("currency_rate")
    'UZS': 12990.20,
    'RUB': 96.89
}

def convert_currency(base, target, amount):
    valid_currencies = exchange_rates.keys()
    if base not in valid_currencies or target not in valid_currencies:
        raise ValueError("Invalid currency type")
    base_to_target_rate = exchange_rates[target] / exchange_rates[base]
    converted_amount = amount * base_to_target_rate
    return round(converted_amount, 2)



