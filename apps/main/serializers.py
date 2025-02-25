from rest_framework import serializers
from .models import Acquaintance, MoneyCirculation, Income, Expense, DailyRemainder


class AcquaintanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Acquaintance
        fields = ['id', 'first_name', 'last_name', 'description', 'phone_number', 'extra_phone_number',
                  'landing', 'debt', 'currency_type', 'updated_at', 'created_at']
        read_only_fields = ['landing', 'debt', 'updated_at', 'created_at']


class MoneyCirculationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoneyCirculation
        fields = ['id', 'acquaintance', 'amount', 'description', 'currency_type', 'type', 'updated_at', 'created_at']
        read_only_fields = ['type', 'updated_at', 'created_at']


class AcquaintanceDetailSerializer(serializers.ModelSerializer):
    circulations = MoneyCirculationSerializer(source="moneycirculation_set", many=True)
    class Meta:
        model = Acquaintance
        fields = ['id', 'first_name', 'last_name', 'description', 'phone_number', 'extra_phone_number',
                  'landing', 'debt', 'currency_type', 'updated_at', 'created_at', 'circulations']


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['id', 'reason', 'description', 'amount', 'currency_type', 'updated_at', 'created_at', 'user', 'section']
        read_only_fields = ['updated_at', 'created_at', 'user', 'section']

class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = ['id', 'reason', 'description', 'amount', 'currency_type', 'updated_at', 'created_at', 'user', 'section']
        read_only_fields = ['updated_at', 'created_at', 'user', 'section']


class DailyRemainderSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyRemainder
        fields = ['id', 'amount', 'created_at']


################################

class MixedDataSerializer(serializers.Serializer):
    created_at = serializers.DateTimeField()
    description = serializers.CharField()
    amount = serializers.FloatField()
    currency_type = serializers.CharField()