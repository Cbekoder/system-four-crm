from rest_framework.exceptions import ValidationError
from rest_framework.relations import StringRelatedField
from rest_framework.serializers import ModelSerializer, DateTimeField, PrimaryKeyRelatedField, SerializerMethodField
from django.utils import timezone

from .models import (
    Driver, Tenant, Contractor, Car, Trailer, CarExpense, LogisticSalaryPayment,
    TIR, TIRRecord, Company, Waybill, ContractRecord, ContractCars, ContractIncome, WaybillPayout
)
from ..main.serializers import IncomeSerializer


# Driver serilizers
class DriverSerializer(ModelSerializer):
    created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    updated_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)

    class Meta:
        model = Driver
        fields = ['id', 'first_name', 'last_name', 'middle_name', 'phone_number', 'extra_phone_number', 'birth_date',
                  'description', 'balance', 'currency_type', 'licence', 'passport', 'given_place', 'given_date',
                  'address', 'updated_at', 'created_at']
        read_only_fields = ['balance', 'updated_at', 'created_at']


# Tenant serializers
class TenantSerializer(ModelSerializer):
    created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    updated_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)

    class Meta:
        model = Tenant
        fields = ['id', 'first_name', 'last_name', 'description', 'phone_number', 'extra_phone_number',
                  'landing', 'currency_type', 'updated_at', 'created_at']
        read_only_fields = ['updated_at', 'created_at']


# Contractor serializer
class ContractorSerializer(ModelSerializer):
    created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    updated_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)

    class Meta:
        model = Contractor
        fields = ['id', 'name', 'inn', 'phone_number', 'extra_phone_number',
                  'landing', 'currency_type', 'updated_at', 'created_at']
        read_only_fields = ['landing', 'updated_at', 'created_at']

# Car serializer
class CarSerializer(ModelSerializer):
    created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    updated_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)

    class Meta:
        model = Car
        fields = ['id', 'brand', 'model', 'state_number', 'year', 'color', 'tech_passport', 'is_active', 'tenant',
                  'updated_at', 'created_at']
        read_only_fields = ['updated_at', 'created_at']


# Trailer serializer
class TrailerSerializer(ModelSerializer):
    created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    updated_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)

    class Meta:
        model = Trailer
        fields = ['id', 'model', 'state_number', 'year', 'color', 'tech_passport', 'car', 'updated_at', 'created_at']
        read_only_fields = ['updated_at', 'created_at']


# TIR serializer
class TIRSerializer(ModelSerializer):
    created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    updated_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    class Meta:
        model = TIR
        fields = ['id', 'serial_number', 'get_date', 'deadline', 'status', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


# Company serializer
class CompanySerializer(ModelSerializer):
    created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    updated_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    class Meta:
        model = Company
        fields = ['id', 'name', 'director', 'inn', 'xp', 'mfo', 'phone_number', 'email', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


# Waybill serializer
class WaybillSerializer(ModelSerializer):
    class Meta:
        model = Waybill
        fields = [
            'id', 'departure_date', 'arrival_date', 'driver_1', 'driver_2', 'car', 'trailer', 'company'
        ]

    def validate(self, data):
        if data.get('arrival_date') and data['arrival_date'] < data['departure_date']:
            raise ValidationError("Arrival date cannot be earlier than departure date.")
        return data


class WaybillPayoutSerializer(ModelSerializer):
    creator = StringRelatedField()
    class Meta:
        model = WaybillPayout
        fields = ['id', 'amount', 'currency_type', 'description', 'date', 'creator']


class WaybillDetailSerailizer(ModelSerializer):
    driver_1 = DriverSerializer()
    driver_2 = DriverSerializer()
    car = CarSerializer()
    trailer = TrailerSerializer()
    company = CompanySerializer()
    created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    updated_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    payouts = WaybillPayoutSerializer(many=True, read_only=True)
    class Meta:
        model = Waybill
        fields = ['id', 'departure_date', 'arrival_date', 'driver_1', 'driver_2', 'car', 'trailer', 'company', 'created_at', 'updated_at', 'payouts']


class WaybillPayoutCreateSerializer(ModelSerializer):
    class Meta:
        model = WaybillPayout
        fields = ['id', 'waybill', 'amount', 'currency_type', 'description', 'creator', 'date']


class WaybillPayoutDetailSerializer(ModelSerializer):
    waybill = WaybillSerializer()
    creator = StringRelatedField()
    class Meta:
        model = WaybillPayout
        fields = ['id', 'waybill', 'amount', 'currency_type', 'description', 'creator', 'date']



# TIR Record serializers
class TIRRecordSerializer(ModelSerializer):
    created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    updated_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    tir = PrimaryKeyRelatedField(queryset=TIR.objects.all(), allow_null=False)
    waybill = PrimaryKeyRelatedField(queryset=Waybill.objects.all(), allow_null=False)

    class Meta:
        model = TIRRecord
        fields = ['id', 'tir', 'waybill', 'tir_get_date', 'tir_deadline', 'status', 'updated_at', 'created_at']
        read_only_fields = ('creator', 'status')


class TIRRecordDetailSerializer(ModelSerializer):
    created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    updated_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    tir = TIRSerializer()
    waybill = WaybillSerializer()
    days_left = SerializerMethodField()

    class Meta:
        model = TIRRecord
        fields = ['id', 'tir', 'waybill', 'tir_get_date', 'tir_deadline', 'days_left', 'status', 'is_returned',
                  'creator', 'updated_at', 'created_at']

    def get_days_left(self, obj):
        if obj.is_returned:
            return 0
        if obj.submission_deadline:
            today = timezone.now().date()
            return max((obj.submission_deadline - today).days, 0)
        return None


class TIRRecordUpdateSerializer(ModelSerializer):
    created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    updated_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)

    class Meta:
        model = TIRRecord
        fields = ['id', 'tir', 'waybill', 'tir_get_date', 'tir_deadline', 'status', 'is_returned', 'creator',
                  'updated_at', 'created_at']
        read_only_fields = ('creator', 'updated_at', 'created_at')


# Contract serializers
class ContractCarsCreateSerailizer(ModelSerializer):
    car = PrimaryKeyRelatedField(queryset=Car.objects.all(), allow_null=False)
    trailer = PrimaryKeyRelatedField(queryset=Trailer.objects.all(), allow_null=False)

    class Meta:
        model = ContractCars
        fields = ['id', 'car', 'trailer']


class ContractCarsDetailSerializer(ModelSerializer):
    car = CarSerializer()
    trailer = TrailerSerializer()

    class Meta:
        model = ContractCars
        fields = ['id', 'car', 'trailer']


class ContractIncomeDetailSerializer(ModelSerializer):
    class Meta:
        model = ContractIncome
        fields = ['id', 'amount', 'currency_type', 'date', 'bank_name']


class ContractRecordCreateSerializer(ModelSerializer):
    contractor = PrimaryKeyRelatedField(queryset=Contractor.objects.all(), allow_null=True)
    cars = ContractCarsCreateSerailizer(many=True)

    class Meta:
        model = ContractRecord
        fields = [
            'id', 'contract_number', 'date', 'invoice_number',
            'contractor', 'description', 'amount', 'currency_type',
            'remaining', 'status', 'cars'
        ]
        read_only_fields = ['status']  # Status is managed by save logic in some cases

    def validate(self, data):
        """Custom validation for required fields and logic."""
        if not data.get('contractor'):
            raise ValidationError("Contractor majburiy ravishda kiritilishi kerak.")
        if data.get('amount') is not None and data['amount'] < 0:
            raise ValidationError("Amount must be a positive value.")
        return data

    # def create(self, validated_data):
    #     """Override to handle custom save logic."""
    #     request = self.context.get('request')
    #     creator = request.user if request and hasattr(request, 'user') else None
    #
    #     # Create the instance without saving to DB yet
    #     contract_record = ContractRecord(**validated_data)
    #     contract_record.creator = creator  # Assuming creator is a ForeignKey to User
    #
    #     # Call the model's save method to trigger custom logic
    #     contract_record.save()
    #     return contract_record
    #
    # def update(self, instance, validated_data):
    #     """Override to handle updates while respecting save logic."""
    #     request = self.context.get('request')
    #     instance.creator = request.user if request and hasattr(request, 'user') else instance.creator
    #
    #     # Update fields
    #     for attr, value in validated_data.items():
    #         setattr(instance, attr, value)
    #
    #     # Call the model's save method
    #     instance.save()
    #     return instance


class ContractRecordDetailSerializer(ModelSerializer):
    contractor = PrimaryKeyRelatedField(queryset=Contractor.objects.all(), allow_null=True)
    cars = ContractCarsDetailSerializer(source="contractcars_set", many=True, read_only=True)
    incomes = ContractIncomeDetailSerializer(source="contractincome_set", many=True, read_only=True)

    class Meta:
        model = ContractRecord
        fields = [
            'id', 'contract_number', 'date', 'invoice_number',
            'contractor', 'description', 'amount', 'currency_type',
            'remaining', 'status', 'cars', 'incomes'
        ]


class ContractIncomeCreateSerializer(ModelSerializer):
    class Meta:
        model = ContractIncome
        fields = ['id', 'contract', 'amount', 'currency_type', 'date', 'bank_name', 'created_at']
        read_only_fields = ['created_at']

class ContractIncomeFullDetailSerializer(ModelSerializer):
    contract = ContractRecordDetailSerializer()
    class Meta:
        model = ContractIncome
        fields = ['id', 'contract', 'amount', 'currency_type', 'date', 'bank_name', 'created_at']
        read_only_fields = ['created_at']


# Car expense serializer
class CarExpenseSerializer(ModelSerializer):
    created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    updated_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)

    class Meta:
        model = CarExpense
        fields = ['id', 'car', 'trailer', 'reason', 'description', 'amount', 'status', 'currency_type', 'updated_at',
                  'created_at']
        read_only_fields = ['status', 'updated_at', 'created_at']


# Driver serializer
class DriverLogisticSalaryPaymentSerializer(ModelSerializer):
    created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    updated_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)

    class Meta:
        model = LogisticSalaryPayment
        fields = ['id', 'driver', 'description', 'amount', 'currency_type', 'status', 'updated_at', 'created_at']
        read_only_fields = ['status', 'updated_at', 'created_at']
