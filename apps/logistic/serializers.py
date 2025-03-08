from rest_framework.serializers import ModelSerializer, DateTimeField
from .models import Driver, Tenant, Contractor, Car, Trailer, CarExpense, SalaryPayment, Contract, Transit, \
    TransitExpense, TransitIncome


class DriverSerializer(ModelSerializer):
    created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    updated_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    class Meta:
        model = Driver
        fields = ['id', 'first_name', 'last_name', 'phone_number', 'extra_phone_number', 'birth_date', 'description',
                  'balance', 'currency_type', 'updated_at', 'created_at']
        read_only_fields = ['balance', 'updated_at', 'created_at']


class TenantSerializer(ModelSerializer):
    created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    updated_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    class Meta:
        model = Tenant
        fields = ['id', 'first_name', 'last_name', 'description', 'phone_number', 'extra_phone_number',
                  'landing', 'currency_type', 'updated_at', 'created_at']
        read_only_fields = ['updated_at', 'created_at']


class ContractorSerializer(ModelSerializer):
    created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    updated_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    class Meta:
        model = Contractor
        fields = ['id', 'first_name', 'last_name', 'description', 'phone_number', 'extra_phone_number',
                  'landing', 'currency_type', 'updated_at', 'created_at']
        read_only_fields = ['landing', 'updated_at', 'created_at']


class CarSerializer(ModelSerializer):
    created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    updated_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    class Meta:
        model = Car
        fields = ['id', 'brand', 'model', 'state_number', 'year', 'color', 'tech_passport', 'is_active', 'tenant',
                  'updated_at', 'created_at']
        read_only_fields = ['updated_at', 'created_at']


class TrailerSerializer(ModelSerializer):
    created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    updated_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    class Meta:
        model = Trailer
        fields = ['id', 'model', 'state_number', 'year', 'color', 'tech_passport', 'car', 'updated_at', 'created_at']
        read_only_fields = ['updated_at', 'created_at']


class CarExpenseSerializer(ModelSerializer):
    created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    updated_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    class Meta:
        model = CarExpense
        fields = ['id', 'car', 'trailer', 'reason', 'description', 'amount', 'status', 'currency_type', 'updated_at',
                  'created_at']
        read_only_fields = ['status', 'updated_at', 'created_at']


class DriverSalaryPaymentSerializer(ModelSerializer):
    created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    updated_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    class Meta:
        model = SalaryPayment
        fields = ['id', 'driver', 'description', 'amount', 'currency_type', 'status', 'updated_at', 'created_at']
        read_only_fields = ['status', 'updated_at', 'created_at']


class ContractSerializer(ModelSerializer):
    created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    updated_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    class Meta:
        model = Contract
        fields = ['id', 'contract_id', 'contractor', 'status', 'updated_at', 'created_at']
        read_only_fields = ['status', 'updated_at', 'created_at']


class TransitPostSerializer(ModelSerializer):
    created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    updated_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    class Meta:
        model = Transit
        fields = ['id', 'car', 'driver', 'leaving_contract', 'leaving_amount', 'leaving_date', 'arrival_contract',
                  'arrival_amount', 'arrival_date', 'driver_fee', 'status', 'updated_at', 'created_at']
        read_only_fields = ['updated_at', 'created_at']

class TransitGetSerializer(ModelSerializer):
    car = CarSerializer()
    driver = DriverSerializer()
    leaving_contract = ContractSerializer()
    arrival_contract = ContractSerializer()
    created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    updated_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    class Meta:
        model = Transit
        fields = ['id', 'car', 'driver', 'leaving_contract', 'leaving_amount', 'leaving_date', 'arrival_contract',
                  'arrival_amount', 'arrival_date', 'driver_fee', 'status', 'updated_at', 'created_at']
        read_only_fields = ['updated_at', 'created_at']


class TransitExpenseSerializer(ModelSerializer):
    created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    updated_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    class Meta:
        model = TransitExpense
        fields = ['id', 'transit', 'reason', 'description', 'amount', 'transfer_type', 'currency_type','status',
                  'updated_at', 'created_at']
        read_only_fields = ['status', 'updated_at', 'created_at']


class TransitIncomeSerializer(ModelSerializer):
    created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    updated_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    class Meta:
        model = TransitIncome
        fields = ['id', 'transit', 'reason', 'description', 'amount', 'transfer_type', 'currency_type','status',
                  'updated_at', 'created_at']
        read_only_fields = ['status', 'updated_at', 'created_at']
        

class TransitDetailSerializer(ModelSerializer):
    car = CarSerializer()
    driver = DriverSerializer()
    leaving_contract = ContractSerializer()
    arrival_contract = ContractSerializer()
    expenses = TransitExpenseSerializer(many=True, source="expenses_set")
    incomes = TransitIncomeSerializer(many=True, source="incomes_set")
    created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    updated_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    class Meta:
        model = Transit
        fields = ['id', 'car', 'driver', 'leaving_contract', 'leaving_amount', 'leaving_date', 'arrival_contract',
                  'arrival_amount', 'arrival_date', 'driver_fee', 'status', 'updated_at', 'created_at', 'expenses', 'incomes']
