from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField, DateTimeField
from .models import *
from apps.main.models import Expense,Income
from apps.main.serializers import ExpenseSerializer
from apps.common.models import SECTION_CHOICES


class RefrigeratorSerializer(ModelSerializer):
    created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    updated_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    class Meta:
        model = Refrigerator
        fields = '__all__'


class RefrigeratorDetailSerializer(ModelSerializer):
    expenses = SerializerMethodField()
    electricity_bills = SerializerMethodField()
    created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    updated_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    class Meta:
        model = Refrigerator
        fields = '__all__'

    def get_expenses(self, obj):
        expenses = Expense.objects.filter(section='fridge', reason=f"expense|{obj.id}")
        return ExpenseSerializer(expenses, many=True).data

    def get_electricity_bills(self, obj):
        bills = Expense.objects.filter(section='fridge', reason=f'electricity|{obj.id}')
        serializer = ExpenseSerializer(bills, many=True)

        serialized_data = serializer.data
        for expense in serialized_data:
            expense.pop('reason', None)
        return serialized_data


class ElectricityBillPostSerializer(ModelSerializer):
    refrigerator = PrimaryKeyRelatedField(
        queryset=Refrigerator.objects.all(), write_only=True, required=True
    )
    created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    updated_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    class Meta:
        model = Expense
        fields = '__all__'
        extra_kwargs = {'reason': {'read_only': True}}

    def create(self, validated_data):
        refrigerator = validated_data.pop('refrigerator')
        validated_data['reason'] = f"electricity|{refrigerator.id}"
        return super().create(validated_data)

class ElectricityBillSerializer(ModelSerializer):
    refrigerator = SerializerMethodField()
    created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    updated_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    class Meta:
        model = Expense
        fields = ['id', 'refrigerator', 'description', 'amount', 'currency_type', 'status', 'updated_at', 'created_at']
        read_only_fields = ['status']

    def get_refrigerator(self, obj):
        try:
            reason, refrigerator_id = map(str, obj.reason.split("|"))
            refrigerator = Refrigerator.objects.get(id=refrigerator_id)
            return RefrigeratorSerializer(refrigerator).data
        except Refrigerator.DoesNotExist:
            return None  # Return None if ref


class FridgeExpensePostSerializer(ModelSerializer):
    refrigerator = PrimaryKeyRelatedField(
        queryset=Refrigerator.objects.all(), write_only=True, required=True
    )
    created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    updated_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    class Meta:
        model = Expense
        fields = ['id', 'refrigerator', 'description', 'amount', 'currency_type', 'section', 'status', 'updated_at', 'created_at']
        read_only_fields = ['updated_at', 'created_at', 'status', 'section']

    def create(self, validated_data):
        refrigerator = validated_data.pop('refrigerator')
        validated_data['reason'] = f"expense|{refrigerator.id}"
        return super().create(validated_data)

class FridgeExpenseSerializer(ModelSerializer):
    refrigerator = SerializerMethodField()
    created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    updated_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    class Meta:
        model = Expense
        fields = ['id', 'refrigerator', 'description', 'amount', 'currency_type', 'status', 'section', 'updated_at', 'created_at']
        read_only_fields = ['status', 'section']

    def get_refrigerator(self, obj):
        try:
            reason, refrigerator_id = map(str, obj.reason.split("|"))
            refrigerator = Refrigerator.objects.get(id=refrigerator_id)
            return RefrigeratorSerializer(refrigerator).data
        except Refrigerator.DoesNotExist:
            return None

class FridgeIncomeSerializer(ModelSerializer):
    refrigerator = SerializerMethodField()
    created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    updated_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    class Meta:
        model = Income
        fields = ['id', 'refrigerator', 'description', 'amount', 'currency_type', 'section', 'status', 'updated_at', 'created_at']
        read_only_fields = ['status', 'section']

    def get_refrigerator(self, obj):
        try:
            reason, refrigerator_id = map(str, obj.reason.split("|"))
            refrigerator = Refrigerator.objects.get(id=refrigerator_id)
            return RefrigeratorSerializer(refrigerator).data
        except Refrigerator.DoesNotExist:
            return None

class FridgeIncomePostSerializer(ModelSerializer):
    refrigerator = PrimaryKeyRelatedField(
        queryset=Refrigerator.objects.all(), write_only=True, required=True
    )
    created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    updated_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    class Meta:
        model = Income
        fields = ['id', 'refrigerator', 'description', 'amount', 'currency_type', 'status', 'section', 'updated_at', 'created_at']
        read_only_fields = ['updated_at', 'created_at', 'status', 'section']

    def create(self, validated_data):
        refrigerator = validated_data.pop('refrigerator')
        validated_data['reason'] = f"income|{refrigerator.id}"
        return super().create(validated_data)

