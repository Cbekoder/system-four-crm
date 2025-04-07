from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from django.db.models import Case, When, Value, CharField

from apps.common.services.logging import Telegram
from apps.common.utils import fetch_currency_rate
from apps.main.utils import calculate_remainder
from apps.main.models import DailyRemainder
from apps.logistic.models import ContractRecord
from apps.users.models import User


class Command(BaseCommand):
    help = 'Run daily tasks at 00:00'

    def update_contract_status(self):
        today = timezone.now().date()

        three_days_ago = today - timedelta(days=3)
        seven_days_ago = today - timedelta(days=7)

        ContractRecord.objects.update(
            status=Case(
                When(remaining=0, then=Value('accepted')),
                When(date__lt=seven_days_ago, then=Value('warning')),
                When(date__lt=three_days_ago, date__gte=seven_days_ago, then=Value('waiting')),
                When(date__gte=three_days_ago, then=Value('new')),
                default=Value('new'),
                output_field=CharField()
            )
        )

    def save_user_remainder(self):
        for user in User.objects.all():
            DailyRemainder.objects.create(
                user=user,
                amount=round(user.balance, 2),
                currency_type=user.currency_type
            )

    def handle(self, *args, **kwargs):

        self.save_user_remainder()
        Telegram.send_log("Фойдаланувчиларнинг кунлик қолдиқлари сақланди.✅")
        self.stdout.write(self.style.SUCCESS('DailyRemainder records created!'))

        # Update ContractRecord statuses
        self.update_contract_status()
        Telegram.send_log("Шартномаларнинг ҳолатлари янгиланди.✅")

        self.stdout.write(self.style.SUCCESS(f"Contract statuses updated on {timezone.now().date()}"))


        self.stdout.write(self.style.SUCCESS('Daily tasks completed!'))