from rest_framework import serializers
from .models import *
from apps.main.models import Expense


class SalaryPaymentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalaryPayment
        fields = ['description', 'amount', 'currency_type', 'updated_at', 'created_at']

class GardenerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gardener
        fields = ['id', 'first_name', 'last_name', 'phone_number', 'extra_phone_number', 'birth_date', 'description',
                  'balance', 'currency_type', 'updated_at', 'created_at',]
        read_only_fields = ['balance', 'updated_at', 'created_at']

class GardenerDetailSerializer(serializers.ModelSerializer):
    salaries = SalaryPaymentDetailSerializer(source="salarypayment_set", many=True)
    class Meta:
        model = Gardener
        fields = ['id', 'first_name', 'last_name', 'phone_number', 'extra_phone_number', 'birth_date', 'description',
                  'balance', 'currency_type', 'updated_at', 'created_at', 'salaries']
        read_only_fields = ['balance', 'updated_at', 'created_at']


class GardenerSalaryPaymentGetSerializer(serializers.ModelSerializer):
    gardener = GardenerSerializer()
    class Meta:
        model = SalaryPayment
        fields = ['gardener','description', 'amount', 'currency_type', 'updated_at', 'created_at']


class GardenerSalaryPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalaryPayment
        fields = ['description', 'amount', 'currency_type', 'updated_at', 'created_at']

    # def create(self, validated_data):
        # salary_payment = SalaryPayment.objects.create(**validated_data)
        #
        # Expense.objects.create(
        #     reason="Bog'bonning oylik maoshi",
        #     description=validated_data.get("description", ""),
        #     amount=validated_data["amount"],
        #     currency_type=validated_data.get("currency_type", "UZS"),
        #     section="garden",
        #     user=self.context["request"].user if "request" in self.context else None
        # )
        #
        # return salary_payment

