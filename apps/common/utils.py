

exchange_rates = {
    'USD': 1.0,
    'UZS': 12930.0
}

def convert_currency(base, target, amount):
    base_to_target_rate = exchange_rates[target] / exchange_rates[base]
    converted_amount = amount * base_to_target_rate
    return round(converted_amount, 2)