from rest_framework.serializers import ModelSerializer, DateTimeField, Serializer, CharField, FloatField
from rest_framework import serializers
from .models import Acquaintance, MoneyCirculation, Income, Expense, DailyRemainder


class AcquaintanceSerializer(ModelSerializer):
    created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    updated_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    class Meta:
        model = Acquaintance
        fields = ['id', 'first_name', 'last_name', 'description', 'phone_number', 'extra_phone_number',
                  'landing', 'debt', 'currency_type', 'updated_at', 'created_at']
        read_only_fields = ['landing', 'debt', 'updated_at', 'created_at']


class MoneyCirculationSerializer(ModelSerializer):
    created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    updated_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    class Meta:
        model = MoneyCirculation
        fields = ['id', 'acquaintance', 'amount', 'description', 'currency_type', 'type', 'updated_at', 'created_at']
        read_only_fields = ['type', 'updated_at', 'created_at']


class AcquaintanceDetailSerializer(ModelSerializer):
    circulations = MoneyCirculationSerializer(source="moneycirculation_set", many=True)
    created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    updated_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    class Meta:
        model = Acquaintance
        fields = ['id', 'first_name', 'last_name', 'description', 'phone_number', 'extra_phone_number',
                  'landing', 'debt', 'currency_type', 'updated_at', 'created_at', 'circulations']


class ExpenseSerializer(ModelSerializer):
    created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    updated_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    class Meta:
        model = Expense
        fields = ['id', 'reason', 'description', 'amount', 'currency_type', 'updated_at', 'created_at', 'user', 'section']
        read_only_fields = ['updated_at', 'created_at', 'user', 'section']

class IncomeSerializer(ModelSerializer):
    created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    updated_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    class Meta:
        model = Income
        fields = ['id', 'reason', 'description', 'amount', 'currency_type', 'updated_at', 'created_at', 'user', 'section']
        read_only_fields = ['updated_at', 'created_at', 'user', 'section']


class DailyRemainderSerializer(ModelSerializer):
    created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    class Meta:
        model = DailyRemainder
        fields = ['id', 'amount', 'created_at']


################################

class MixedDataSerializer(Serializer):
    created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    description = CharField()
    amount = FloatField()
    currency_type = CharField()

class TransactionVerifyDetailSerializer(serializers.Serializer):
    unique_id = serializers.CharField(max_length=50, read_only=True)
    creator = serializers.CharField(max_length=100, read_only=True)
    description = serializers.CharField(max_length=255, read_only=True)
    amount = serializers.FloatField(read_only=True)
    currency_type = serializers.CharField(max_length=10, read_only=True)
    updated_at = serializers.DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    created_at = serializers.DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)

# POST uchun serializer
class TransactionVerifyActionSerializer(serializers.Serializer):
    unique_id = serializers.CharField(max_length=50, required=True)
    action = serializers.ChoiceField(choices=['verify', 'cancel'], required=True)