from rest_framework.serializers import ModelSerializer
from .models import *
from apps.common.models import SECTION_CHOICES


class RefrigeratorSerializer(ModelSerializer):
    class Meta:
        model = Refrigerator
        fields = '__all__'

class ElectricityBillSerializer(ModelSerializer):
    class Meta:
        model = ElectricityBill
        fields = '__all__'

    def create(self, validated_data):
        request = self.context['request']
        # garden_section, _ = Section.objects.get_or_create(name="Muzlatgish(Xolodilnik)")
        # validated_data['section'] = garden_section
        instance = super().create(validated_data)

        Expense.objects.create(
            amount=instance.amount,
            section=SECTION_CHOICES[1][1],
            description=instance.description,
            reason="Muzlatich(xolodilnik) uchun elektr energiya to'lovi",
            currency_type="UZS",
            user=request.user
        )

        return instance


class FridgeExpenseSerializer(ModelSerializer):
    class Meta:
        model = FridgeExpense
        fields = '__all__'

    def create(self, validated_data):
        request = self.context['request']

        validated_data['section'] = SECTION_CHOICES[1][1]
        validated_data['user'] = request.user

        return super().create(validated_data)