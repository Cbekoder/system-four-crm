from rest_framework import serializers
from .models import *
from apps.common.models import SECTION_CHOICES


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
        fields = '__all__'


class GardenerSalaryPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalaryPayment
        fields = '__all__'

