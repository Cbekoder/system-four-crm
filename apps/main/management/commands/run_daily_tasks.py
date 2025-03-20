from django.core.management.base import BaseCommand
from apps.common.utils import fetch_currency_rate
from apps.main.utils import calculate_remainder
from apps.main.models import DailyRemainder
from django.utils import timezone
from apps.users.models import User


class Command(BaseCommand):
    help = 'Run daily tasks at 00:00'

    def handle(self, *args, **kwargs):
        fetch_currency_rate()
        # last_remainder = DailyRemainder.objects.last()
        # user = User.objects.filter(role="CEO").first()
        # DailyRemainder.objects.create(amount=(last_remainder.amount+calculate_remainder(timezone.now().date(), user)), type='auto')
        self.stdout.write(self.style.SUCCESS('Daily tasks completed!'))