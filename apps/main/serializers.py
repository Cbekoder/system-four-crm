from rest_framework.serializers import ModelSerializer, DateTimeField, Serializer, CharField, FloatField
from rest_framework import serializers
from tutorial.quickstart.serializers import UserSerializer

from .models import Acquaintance, MoneyCirculation, Income, Expense, DailyRemainder, TransactionToAdmin, \
    TransactionToSection

from apps.common.models import CurrencyRate
from apps.users.serializers import UserDetailSerializer

class CurrencyRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrencyRate
        fields = '__all__'
        read_only_fields = ('id', 'creator')

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
    acquaintance = AcquaintanceSerializer(read_only=True)
    class Meta:
        model = MoneyCirculation
        fields = ['id', 'acquaintance', 'amount', 'description', 'currency_type', 'type', 'status', 'updated_at', 'created_at']
        read_only_fields = ['type','status',  'updated_at', 'created_at']


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
        fields = ['id', 'reason', 'description', 'amount', 'currency_type', 'status', 'updated_at', 'created_at', 'user', 'section']
        read_only_fields = ['updated_at', 'created_at', 'user', 'section', 'status']

class IncomeSerializer(ModelSerializer):
    created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    updated_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    class Meta:
        model = Income
        fields = ['id', 'reason', 'description', 'amount', 'currency_type', 'status', 'updated_at', 'created_at', 'user', 'section']
        read_only_fields = ['updated_at', 'created_at', 'user', 'section', 'status']


class TransactionToAdminSerializer(ModelSerializer):
    created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    updated_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    admin = UserDetailSerializer()
    class Meta:
        model = TransactionToAdmin
        fields = '__all__'


class TransactionToAdminCreateSerializer(ModelSerializer):
    class Meta:
        model = TransactionToAdmin
        fields = ('id', 'admin', 'amount', 'currency_type', 'description')


class TransactionToSectionSerializer(ModelSerializer):
    created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    updated_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    class Meta:
        model = TransactionToSection
        fields = '__all__'


class TransactionToSectionCreateSerializer(ModelSerializer):
    class Meta:
        model = TransactionToSection
        fields = ('id', 'section', 'amount', 'currency_type', 'description')



class DailyRemainderSerializer(ModelSerializer):
    created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    class Meta:
        model = DailyRemainder
        fields = ['id', 'amount', 'created_at']


################################

class TransactionHistorySerializer(serializers.Serializer):
    id = serializers.CharField()
    reason = serializers.CharField()
    amount = serializers.FloatField()
    currency_type = serializers.CharField()
    date = serializers.DateField()

class MixedDataSerializer(Serializer):
    id = serializers.CharField()
    section = serializers.CharField()
    reason = serializers.CharField()
    amount = serializers.FloatField()
    currency_type = serializers.CharField()
    date = serializers.DateField()

class TransactionVerifyDetailSerializer(serializers.Serializer):
    unique_id = serializers.CharField(max_length=50, read_only=True)
    creator = serializers.CharField(max_length=100, read_only=True)
    section = serializers.CharField(max_length=100, read_only=True)
    description = serializers.CharField(max_length=255, read_only=True)
    amount = serializers.FloatField(read_only=True)
    currency_type = serializers.CharField(max_length=10, read_only=True)
    updated_at = serializers.DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    created_at = serializers.DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)

# POST uchun serializer
class TransactionVerifyActionSerializer(serializers.Serializer):
    unique_id = serializers.CharField(
        max_length=50,
        required=True,
        help_text="Tranzaksiya uchun unique ID (masalan, FA-BA-32) yoki 'ALL' barcha tranzaksiyalar uchun"
    )
    action = serializers.ChoiceField(
        choices=['verify', 'cancel'],
        required=True,
        help_text="Amal: verify yoki cancel"
    )