from django.core.management.base import BaseCommand
from apps.common.utils import fetch_currency_rate
from apps.main.utils import calculate_remainder
from apps.main.models import DailyRemainder
from django.utils import timezone
from apps.users.models import User


class Command(BaseCommand):
    help = 'Run daily tasks at 00:00'

    def handle(self, *args, **kwargs):

        for user in User.objects.all():
            DailyRemainder.objects.create(
                user=user,
                amount=user.balance,
                currency_type=user.currency_type
            )

        self.stdout.write(self.style.SUCCESS('Daily tasks completed!'))