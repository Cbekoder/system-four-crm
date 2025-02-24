from celery import shared_task
from django.utils.timezone import now, localtime, timedelta
from .models import DailyRemainder  # Adjust import as needed
from .utils import get_remainder_data

@shared_task
def save_daily_remainder():
    """
    This task calculates and saves the daily remainder at 23:59.
    """
    yesterday = localtime(now()).date() - timedelta(days=1)
    start_date = yesterday
    end_date = yesterday

    amount = get_remainder_data(start_date, end_date)

    DailyRemainder.objects.create(amount=amount)
    return f"Daily remainder saved: {amount}"