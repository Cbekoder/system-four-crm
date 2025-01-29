from rest_framework import serializers
from .models import *

class GardenerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gardener
        fields = '__all__'


class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = '__all__'


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'

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

