from django.core.cache import cache
import requests


def fetch_currency_rate():
    response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")

    if response.status_code == 200:
        data = response.json()
        new_rate = data.get("rates", {}).get("UZS")
        if new_rate:
            cache.set("daily_currency_rate", new_rate, timeout=86400)  # Cache for 24 hours
            return f"Rate cached: {new_rate}"
    return "Failed to update rate"
