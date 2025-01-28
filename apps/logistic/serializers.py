from rest_framework import serializers
from .models import Driver, Tenant, Contractor, Car, Trailer, CarExpense, SalaryPayment, Contract, Transit, \
    TransitExpense, TransitIncome


class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ['id', 'first_name', 'last_name', 'phone_number', 'extra_phone_number', 'birth_date', 'description',
                  'balance', 'currency_type', 'updated_at', 'created_at']
        read_only_fields = ['balance', 'updated_at', 'created_at']


class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = ['id', 'first_name', 'last_name', 'description', 'phone_number', 'extra_phone_number',
                  'landing', 'currency_type', 'updated_at', 'created_at']
        read_only_fields = ['updated_at', 'created_at']


class ContractorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contractor
        fields = ['id', 'first_name', 'last_name', 'description', 'phone_number', 'extra_phone_number',
                  'landing', 'currency_type', 'updated_at', 'created_at']
        read_only_fields = ['landing', 'updated_at', 'created_at']


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['id', 'brand', 'model', 'state_number', 'year', 'color', 'tech_passport', 'is_active', 'tenant',
                  'updated_at', 'created_at']
        read_only_fields = ['updated_at', 'created_at']


class TrailerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trailer
        fields = ['id', 'model', 'state_number', 'year', 'color', 'tech_passport', 'car', 'updated_at', 'created_at']
        read_only_fields = ['updated_at', 'created_at']


class CarExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarExpense
        fields = ['id', 'car', 'trailer', 'reason', 'description', 'amount', 'currency_type', 'is_verified', 'updated_at',
                  'created_at']
        read_only_fields = ['updated_at', 'created_at']


class SalaryPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalaryPayment
        fields = ['id', 'driver', 'description', 'amount', 'currency_type', 'is_verified', 'updated_at', 'created_at']
        read_only_fields = ['updated_at', 'created_at']


class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = ['id', 'contract_id', 'contractor', 'updated_at', 'created_at']
        read_only_fields = ['updated_at', 'created_at']


class TransitPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transit
        fields = ['id', 'car', 'driver', 'leaving_contract', 'leaving_amount', 'leaving_date', 'arrival_contract',
                  'arrival_amount', 'arrival_date', 'driver_fee', 'status', 'updated_at', 'created_at']
        read_only_fields = ['updated_at', 'created_at']

class TransitGetSerializer(serializers.ModelSerializer):
    car = CarSerializer()
    driver = DriverSerializer()
    leaving_contract = ContractSerializer()
    arrival_contract = ContractSerializer()
    class Meta:
        model = Transit
        fields = ['id', 'car', 'driver', 'leaving_contract', 'leaving_amount', 'leaving_date', 'arrival_contract',
                  'arrival_amount', 'arrival_date', 'driver_fee', 'status', 'updated_at', 'created_at']
        read_only_fields = ['updated_at', 'created_at']


class TransitExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransitExpense
        fields = ['id', 'transit', 'reason', 'description', 'amount', 'transfer_type', 'currency_type', 'is_verified',
                  'updated_at', 'created_at']
        read_only_fields = ['updated_at', 'created_at']


class TransitIncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransitIncome
        fields = ['id', 'transit', 'reason', 'description', 'amount', 'transfer_type', 'currency_type', 'is_verified',
                  'updated_at', 'created_at']
        read_only_fields = ['updated_at', 'created_at']
        

class TransitDetailSerializer(serializers.ModelSerializer):
    car = CarSerializer()
    driver = DriverSerializer()
    leaving_contract = ContractSerializer()
    arrival_contract = ContractSerializer()
    expenses = TransitExpenseSerializer(many=True, source="expenses_set")
    incomes = TransitIncomeSerializer(many=True, source="incomes_set")
    class Meta:
        model = Transit
        fields = ['id', 'car', 'driver', 'leaving_contract', 'leaving_amount', 'leaving_date', 'arrival_contract',
                  'arrival_amount', 'arrival_date', 'driver_fee', 'status', 'updated_at', 'created_at', 'expenses', 'incomes']
