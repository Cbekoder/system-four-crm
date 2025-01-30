import requests
url="https://cbu.uz/uz/arkhiv-kursov-valyut/json/"

response = requests.get(url)
data = response.json()
data=data[0]
usd_to_uzs_rate= float(data['Rate'])

exchange_rates = {
    'USD': 1.0,
    'UZS': usd_to_uzs_rate
}

def convert_currency(base, target, amount):
    base_to_target_rate = exchange_rates[target] / exchange_rates[base]
    converted_amount = amount * base_to_target_rate
    return round(converted_amount, 2)



