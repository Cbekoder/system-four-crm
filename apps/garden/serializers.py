from rest_framework import serializers
from .models import *
from apps.common.models import SECTION_CHOICES

class GardenerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gardener
        fields = '__all__'


class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = '__all__'

    def create(self, validated_data):
        request = self.context['request']

        # garden_section, _ = Section.objects.get_or_create(name="Bog'")

        validated_data['section'] = SECTION_CHOICES[2][1]
        validated_data['user'] = request.user

        return super().create(validated_data)


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'

    def create(self, validated_data):
        request = self.context['request']

        # garden_section, _ = Section.objects.get_or_create(name="Bog'")
        garden_section=SECTION_CHOICES[2][1]

        validated_data['section'] = garden_section
        validated_data['user'] = request.user

        return super().create(validated_data)

class SalaryPaymentSerializer(serializers.ModelSerializer):
    gardener = GardenerSerializer()
    class Meta:
        model = SalaryPayment
        fields = '__all__'

    # def create(self, validated_data):
    #     gardener = validated_data.get('gardener')
    #     amount = validated_data.get('amount')
    #
    #     if gardener:
    #         # SalaryPayment obyektini yaratamiz
    #         salary_payment = super().create(validated_data)
    #
    #         # Gardener balansini yangilaymiz
    #         print(f"Old balance: {gardener.balance}")  # Debugging
    #         gardener.balance += amount
    #         print(f"New balance: {gardener.balance}")  # Debugging
    #         gardener.save()
    #
    #         return salary_payment
    #     else:
    #         raise serializers.ValidationError({"gardener": "Gardener is required."})

class SalaryPaymentGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalaryPayment
        fields = '__all__'

