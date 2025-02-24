from django.core.cache import cache
import requests
# from .utils import redis


def fetch_currency_rate():
    response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")

    if response.status_code == 200:
        data = response.json()
        UZS_rate = data.get("rates", {}).get("UZS")
        RUB_rate = data.get("rates", {}).get("RUB")
        if UZS_rate and RUB_rate:
            cache.set("UZS_rate", UZS_rate)
            cache.set("RUB_rate", RUB_rate)
            return f"Rate cached: UZS: {UZS_rate}, RUB: {RUB_rate}"
    return "Failed to update rate"
