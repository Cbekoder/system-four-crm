import requests
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist

from apps.common.services.logging import Telegram
from apps.common.models import CurrencyRate

exchange_rates = {
    'USD': 1.0,
    'UZS': cache.get("UZS_rate"),
    'RUB': cache.get("RUB_rate")
}

def convert_currency(base, target, amount):
    if exchange_rates['UZS'] is None or exchange_rates['RUB'] is None:
        try:
            currency_rate = CurrencyRate.objects.latest('created_at')
            cache.set("UZS_rate", currency_rate.usd)
            cache.set("RUB_rate", currency_rate.rub)
            print(cache.get("UZS_rate", currency_rate.usd))
        except ObjectDoesNotExist:
            raise ValueError("Currency rates not found in the database. Please ensure CurrencyRate data exists.")

    valid_currencies = exchange_rates.keys()
    if base not in valid_currencies or target not in valid_currencies:
        raise ValueError(f"Invalid currency type. Supported currencies are {valid_currencies}")
    base_to_target_rate = exchange_rates[target] / exchange_rates[base]
    converted_amount = amount * base_to_target_rate
    return round(converted_amount, 2)

def fetch_currency_rate():
    response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")

    if response.status_code == 200:
        data = response.json()
        UZS_rate = data.get("rates", {}).get("UZS")
        RUB_rate = data.get("rates", {}).get("RUB")
        if UZS_rate and RUB_rate:
            cache.set("UZS_rate", UZS_rate)
            cache.set("RUB_rate", RUB_rate)
            print(cache.get("UZS_rate"))
            Telegram.send_log(f"💸 Янги валюта курслари: \n🇺🇸🔄🇺🇿 USD-UZS: {UZS_rate}, \n🇷🇺🔄🇺🇿 RUB-UZS: {convert_currency('RUB', 'UZS', 1)}")
            return f"Rate cached: UZS: {UZS_rate}, RUB: {RUB_rate}"
    return Telegram.send_log("Валюталар курсини олишда муаммо.")



