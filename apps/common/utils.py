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

def fetch_currency_rate():
    response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")

    if response.status_code == 200:
        data = response.json()
        UZS_rate = data.get("rates", {}).get("UZS")
        RUB_rate = data.get("rates", {}).get("RUB")
        if UZS_rate and RUB_rate:
            cache.set("UZS_rate", UZS_rate)
            cache.set("RUB_rate", RUB_rate)
            Telegram.send_log(f"💸 Янги валюта курслари: \n🇺🇸🔄🇺🇿 USD-UZS: {UZS_rate}, \n🇷🇺🔄🇺🇿 RUB-UZS: {convert_currency('RUB', 'UZS', 1)}")
            return f"Rate cached: UZS: {UZS_rate}, RUB: {RUB_rate}"
    return Telegram.send_log("Валюталар курсини олишда муаммо.")

def validate_currency():
    if exchange_rates['UZS'] is None or exchange_rates['RUB'] is None:
        try:
            currency_rates = CurrencyRate.objects.order_by('created_at')
            if currency_rates.exists():
                currency_rate = currency_rates.last()
                cache.set("UZS_rate", currency_rate.usd)
                cache.set("RUB_rate", currency_rate.rub)
                exchange_rates['UZS'] = currency_rate.usd
                exchange_rates['RUB'] = currency_rate.rub
            else:
                fetch_currency_rate()

        except ObjectDoesNotExist:
            raise ValueError("Currency rates not found in the database. Please ensure CurrencyRate data exists.")


def convert_currency(base, target, amount):
    validate_currency()
    valid_currencies = exchange_rates.keys()
    if base not in valid_currencies or target not in valid_currencies:
        raise ValueError(f"Invalid currency type. Supported currencies are {valid_currencies}")
    base_to_target_rate = exchange_rates[target] / exchange_rates[base]
    converted_amount = amount * base_to_target_rate
    return round(converted_amount, 2)






