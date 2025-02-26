from rest_framework.serializers import ModelSerializer,ValidationError,CharField, DateTimeField
from .models import *
from apps.main.models import Expense, Income

class WorkerSerializer(ModelSerializer):
    created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    updated_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    class Meta:
        model = Worker
        fields = ['id', 'first_name', 'last_name', 'phone_number', 'extra_phone_number', 'birth_date', 'description',
                  'balance', 'currency_type', 'updated_at', 'created_at']

class BasketSerializer(ModelSerializer):
    created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    updated_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    class Meta:
        model = Basket
        fields = ["name", "size", "weight", "quantity", "price", "per_worker_fee", "updated_at", "created_at"]

class SupplierSerializer(ModelSerializer):
    created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    updated_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    class Meta:
        model = Supplier
        fields = '__all__'

class DailyWorkSerializer(ModelSerializer):
    created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    updated_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    class Meta:
        model = DailyWork
        fields = '__all__'

    # def create(self, validated_data):
    #     request = self.context.get('request')
    #
    #     daily_work = DailyWork.objects.create(**validated_data)
    #
    #     Expense.objects.create(
    #         reason="Korzinka | Kunlik ish haqi",
    #         description=daily_work.description,
    #         amount=daily_work.price,
    #         currency_type="UZS",
    #         section="factory",
    #         user=request.user
    #     )
    #
    #     return daily_work

class DailyWorkGetSerializer(ModelSerializer):
    worker = WorkerSerializer()
    created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    updated_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    class Meta:
        model = DailyWork
        fields = '__all__'


class WorkerGetSerializer(ModelSerializer):
    daily_work = DailyWorkSerializer(source="dailywork_set", many=True)
    created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    updated_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    class Meta:
        model = Worker
        fields = '__all__'


class RawMaterialSerializer(ModelSerializer):
    created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    updated_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    class Meta:
        model = RawMaterial
        fields = '__all__'

    # def create(self, validated_data):
    #     request = self.context.get('request')
    #
    #     raw_material = RawMaterial.objects.create(**validated_data)
    #
    #     Expense.objects.create(
    #         reason="Korzinka uchun xomashyo",
    #         description=raw_material.description,
    #         amount=raw_material.price,
    #         currency_type=raw_material.currency_type,
    #         section="factory",
    #         user=request.user
    #     )
    #
    #     return raw_material


class ClientSerializer(ModelSerializer):
    created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    updated_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    class Meta:
        model = Client
        fields = '__all__'

class SaleSerializer(ModelSerializer):
    created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    updated_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    class Meta:
        model = Sale
        fields = '__all__'

    # def create(self, validated_data):
    #     request = self.context.get('request')
    #
    #     sale = Sale.objects.create(**validated_data)
    #
    #     Income.objects.create(
    #         reason=f"Korzinka sotuvi | {sale.client.first_name} {sale.client.last_name}",
    #         description=sale.description,
    #         amount=sale.price,
    #         currency_type=sale.currency_type,
    #         section="factory",
    #         user=request.user
    #     )
    #
    #     return sale


class RawMaterialHistorySerializer(ModelSerializer):
    created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    updated_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    class Meta:
        model = RawMaterialHistory
        fields = '__all__'




