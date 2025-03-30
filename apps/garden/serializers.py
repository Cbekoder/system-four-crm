from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer, DateTimeField
from .models import *
from apps.main.models import Expense, Income
from rest_framework.fields import SerializerMethodField

# Garden Serializers
class GardenSerializer(ModelSerializer):
    class Meta:
        model = Garden
        fields = ['id', 'name','description']


# Gardener Serializers
class GardenerSerializer(ModelSerializer):
    created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    updated_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    class Meta:
        model = Gardener
        fields = ['id', 'first_name', 'last_name', 'phone_number', 'extra_phone_number', 'birth_date', 'description',
                  'balance', 'currency_type', 'updated_at', 'created_at',]
        read_only_fields = ['balance', 'updated_at', 'created_at']

class GardenSalaryPaymentDetailSerializer(ModelSerializer):
    created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    updated_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    class Meta:
        model = GardenSalaryPayment
        fields = ['id', 'description', 'amount', 'currency_type', 'status', 'updated_at', 'created_at']

class GardenerDetailSerializer(ModelSerializer):
    salaries = GardenSalaryPaymentDetailSerializer(source="gardensalarypayment_set", many=True)
    created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    updated_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    class Meta:
        model = Gardener
        fields = ['id', 'first_name', 'last_name', 'phone_number', 'extra_phone_number', 'birth_date', 'description',
                  'balance', 'currency_type', 'updated_at', 'created_at', 'salaries']
        read_only_fields = ['balance', 'updated_at', 'created_at']


# Gardener Salary Payment Serializers
class GardenerSalaryPaymentSerializer(ModelSerializer):
    created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    updated_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    class Meta:
        model = GardenSalaryPayment
        fields = ['id', 'gardener', 'description', 'amount', 'currency_type', 'status', 'updated_at', 'created_at']
        read_only_fields = ['status', 'updated_at', 'created_at']

class GardenerSalaryPaymentGetSerializer(ModelSerializer):
    gardener = GardenerSerializer()
    created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    updated_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    class Meta:
        model = GardenSalaryPayment
        fields = ['id', 'gardener','description', 'amount', 'currency_type', 'status', 'updated_at', 'created_at']
        read_only_fields = ['status', 'updated_at', 'created_at']


# Garden Expense Serializers
class GardenExpensePostSerializer(ModelSerializer):
    created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    updated_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    garden = PrimaryKeyRelatedField(
        queryset=Garden.objects.all(), write_only=True, required=False, allow_null=True
    )

    class Meta:
        model = Expense
        fields = ['id', 'reason', 'description', 'amount', 'currency_type', 'garden', 'status', 'updated_at', 'created_at']
        read_only_fields = ['status', 'updated_at', 'created_at']

    def create(self, validated_data):
        garden = validated_data.pop('garden', None)
        if garden:
            validated_data['reason'] = f"{validated_data.get('reason')} | {garden.name} uchun xarajat | {garden.id}"
        # else:
        #     validated_data['reason'] = "Umumiy xarajat"

        return super().create(validated_data)


class GardenExpenseSerializer(ModelSerializer):
    created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    updated_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    garden = SerializerMethodField()
    class  Meta:
        model = Expense
        fields = ['id', 'reason', 'description', 'amount', 'currency_type','garden', 'description', 'status', 'updated_at', 'created_at']
        read_only_fields = ['status', 'updated_at', 'created_at']

    def get_garden(self, obj):
        try:
            garden_id = int(list(obj.reason.split("|"))[-1])
            garden = Garden.objects.get(id=garden_id)
            return GardenSerializer(garden).data
        except Garden.DoesNotExist:
            return None
        except IndexError:
            return None


# Garden Income Serializers
class GardenIncomePostSerializer(ModelSerializer):
    created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    updated_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    garden = PrimaryKeyRelatedField(
        queryset=Garden.objects.all(), write_only=True, required=False, allow_null=True
    )

    class Meta:
        model = Income
        fields = ['id', 'reason', 'description', 'amount', 'currency_type', 'garden', 'status', 'updated_at', 'created_at']
        read_only_fields = ['status', 'updated_at', 'created_at']

    def create(self, validated_data):
        garden = validated_data.pop('garden', None)
        if garden:
            validated_data['reason'] = f"{validated_data.get('reason')} | {garden.name} учун кирим | {garden.id}"
        # else:
        #     validated_data['reason'] = "Umumiy xarajat"

        return super().create(validated_data)


class GardenIncomeSerializer(ModelSerializer):
    created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    updated_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    garden = SerializerMethodField()
    class  Meta:
        model = Income
        fields = ['id', 'reason', 'description', 'amount', 'currency_type','garden','description', 'status', 'updated_at', 'created_at']
        read_only_fields = ['status', 'updated_at', 'created_at']

    def get_garden(self, obj):
        try:
            garden_id = int(list(obj.reason.split("|"))[1])
            garden = Garden.objects.get(id=garden_id)
            return GardenSerializer(garden).data
        except Garden.DoesNotExist:
            return None
        except IndexError:
            return None


