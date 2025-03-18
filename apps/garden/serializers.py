from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer, DateTimeField
from .models import *
from apps.main.models import Expense
from rest_framework.fields import SerializerMethodField


class GardenSerializer(ModelSerializer):
    class Meta:
        model = Garden
        fields = ['name','description']

class SalaryPaymentDetailSerializer(ModelSerializer):
    created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    updated_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    class Meta:
        model = SalaryPayment
        fields = ['description', 'amount', 'currency_type', 'status', 'updated_at', 'created_at']

class GardenerSerializer(ModelSerializer):
    created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    updated_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    class Meta:
        model = Gardener
        fields = ['id', 'first_name', 'last_name', 'phone_number', 'extra_phone_number', 'birth_date', 'description',
                  'balance', 'currency_type', 'updated_at', 'created_at',]
        read_only_fields = ['balance', 'updated_at', 'created_at']

class GardenerDetailSerializer(ModelSerializer):
    salaries = SalaryPaymentDetailSerializer(source="salarypayment_set", many=True)
    created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    updated_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    class Meta:
        model = Gardener
        fields = ['id', 'first_name', 'last_name', 'phone_number', 'extra_phone_number', 'birth_date', 'description',
                  'balance', 'currency_type', 'updated_at', 'created_at', 'salaries']
        read_only_fields = ['balance', 'updated_at', 'created_at']


class GardenerSalaryPaymentGetSerializer(ModelSerializer):
    gardener = GardenerSerializer()
    created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    updated_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    class Meta:
        model = SalaryPayment
        fields = ['id', 'gardener','description', 'amount', 'currency_type', 'status', 'updated_at', 'created_at']
        read_only_fields = ['status', 'updated_at', 'created_at']


class GardenerSalaryPaymentSerializer(ModelSerializer):
    created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    updated_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    class Meta:
        model = SalaryPayment
        fields = ['gardener', 'description', 'amount', 'currency_type', 'status', 'updated_at', 'created_at']
        read_only_fields = ['status', 'updated_at', 'created_at']

    def create(self, validated_data):
        salary_payment = SalaryPayment.objects.create(**validated_data)

        Expense.objects.create(
            reason="Bog'bonning oylik maoshi",
            description=validated_data.get("description", ""),
            amount=validated_data["amount"],
            currency_type=validated_data.get("currency_type", "UZS"),
            section="garden",
            user=self.context["request"].user if "request" in self.context else None
        )

        return salary_payment

class GardenExpensePostSerializer(ModelSerializer):
    garden = PrimaryKeyRelatedField(
        queryset=Garden.objects.all(), write_only=True, required=True
    )
    class Meta:
        model = Expense
        fields = ['description', 'amount', 'currency_type','garden', 'status', 'updated_at', 'created_at']
        read_only_fields = ['status', 'updated_at', 'created_at']

    def create(self, validated_data):
        garden = validated_data.pop('garden')
        validated_data['reason'] = f"{garden.id}"
        return super().create(validated_data)

class GardenExpenseSerializer(ModelSerializer):
    garden = SerializerMethodField()
    class  Meta:
        model = Expense
        fields = ['description', 'amount', 'currency_type','garden','reason','description', 'status', 'updated_at', 'created_at']
        read_only_fields = ['status', 'updated_at', 'created_at']

    def get_garden(self, obj):
        try:
            garden_id = int(list(obj.reason.split("|"))[1])
            garden = Garden.objects.get(id=1)
            return GardenSerializer(garden).data
        except Garden.DoesNotExist:
            return None
        except IndexError:
            return None


