from django.db import transaction
from rest_framework.exceptions import ValidationError
from rest_framework.relations import StringRelatedField
from rest_framework.serializers import (ModelSerializer, DateTimeField, PrimaryKeyRelatedField, SerializerMethodField,
                                        ListField, CharField)
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
class TIRGetSerializer(ModelSerializer):
    created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    updated_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    class Meta:
        model = TIR
        fields = ['id', 'get_date', 'deadline', 'serial_number', 'status', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class TIRSerializer(ModelSerializer):
    created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    updated_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    serial_numbers = ListField(
        child=CharField(max_length=100),
        write_only=True
    )
    class Meta:
        model = TIR
        fields = ['id', 'get_date', 'deadline', 'status', 'serial_numbers', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def validate(self, data):
        if not data.get('serial_numbers'):
            raise ValidationError("Serial number ro'yxati bo'sh bo'lmasligi kerak.")
        if data.get('get_date') and data.get('deadline') and data['get_date'] > data['deadline']:
            raise ValidationError("Get_date deadline dan katta bo'lmasligi kerak.")
        return data

    def create(self, validated_data):

        serial_numbers = validated_data.pop('serial_numbers', [])


        tir_instances = []
        with transaction.atomic():
            for serial_num in serial_numbers:
                tir = TIR.objects.create(
                    serial_number=serial_num,
                    **validated_data
                )
                tir_instances.append(tir)

        return tir_instances[0] if tir_instances else None

    def to_representation(self, instance):

        representation = super().to_representation(instance)
        representation['serial_numbers'] = instance.serial_number
        return representation


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
        if obj.tir_deadline:
            today = timezone.now().date()
            return max((obj.tir_deadline - today).days, 0)
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


class ContractRecordDetailSerializer(ModelSerializer):
    contractor = ContractorSerializer()
    one_percent = SerializerMethodField()
    cars = ContractCarsDetailSerializer(source="contractcars_set", many=True, read_only=True)
    incomes = ContractIncomeDetailSerializer(source="contractincome_set", many=True, read_only=True)

    class Meta:
        model = ContractRecord
        fields = [
            'id', 'contract_number', 'date', 'invoice_number',
            'contractor', 'description', 'amount', 'currency_type',
            'remaining', 'one_percent', 'status', 'cars', 'incomes'
        ]

    def get_one_percent(self, obj):
        return obj.amount / 100


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
        read_only_fields = ['status', 'remaining']

    def validate(self, data):
        if not data.get('contractor'):
            raise ValidationError("Contractor majburiy ravishda kiritilishi kerak.")
        if data.get('amount') is not None and data['amount'] <= 0:
            raise ValidationError("Amount must be a positive value.")
        return data

    def create(self, validated_data):
        with transaction.atomic():
            cars_data = validated_data.pop('cars', [])
            validated_data['remaining'] = validated_data.get('amount', 0)
            contract_record = ContractRecord.objects.create(**validated_data)
            serialized_cars = []
            for car_data in cars_data:
                car_obj = ContractCars.objects.create(contract=contract_record, **car_data)
                serialized_cars.append(car_obj)
            contract_record.cars = serialized_cars

            return contract_record

    def update(self, instance, validated_data):
        with transaction.atomic():
            cars_data = validated_data.pop('cars', None)
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()

            if cars_data is not None:
                existing_cars = {car.id: car for car in ContractCars.objects.filter(contract=instance)}
                new_car_ids = set()
                serialized_cars = []

                for car_data in cars_data:
                    car_id = car_data.get('id', None)
                    if car_id and car_id in existing_cars:
                        car_obj = existing_cars[car_id]
                        for key, value in car_data.items():
                            setattr(car_obj, key, value)
                        car_obj.save()
                        new_car_ids.add(car_id)
                    else:
                        car_obj = ContractCars.objects.create(contract=instance, **car_data)
                        new_car_ids.add(car_obj.id)
                    serialized_cars.append(car_obj)

                for car_id, car in existing_cars.items():
                    if car_id not in new_car_ids:
                        car.delete()

                instance.cars = serialized_cars

            return instance


class ContractIncomeCreateSerializer(ModelSerializer):
    class Meta:
        model = ContractIncome
        fields = ['id', 'contract', 'amount', 'currency_type', 'date', 'bank_name', 'creator', 'created_at']
        read_only_fields = ['creator', 'created_at']

class ContractIncomeFullDetailSerializer(ModelSerializer):
    contract = ContractRecordDetailSerializer()
    class Meta:
        model = ContractIncome
        fields = ['id', 'contract', 'amount', 'currency_type', 'date', 'bank_name', 'created_at']
        read_only_fields = ['created_at']

class ContractIncomeSimplaDetailSerializer(ModelSerializer):
    class Meta:
        model = ContractIncome
        fields = ['id', 'amount', 'currency_type', 'date', 'bank_name', 'created_at']


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
