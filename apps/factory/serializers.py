from rest_framework.serializers import ModelSerializer, ValidationError, CharField, DateTimeField, \
    PrimaryKeyRelatedField, SerializerMethodField
from .models import *
from apps.main.models import Expense, Income


class WorkerSerializer(ModelSerializer):
    created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    updated_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)

    class Meta:
        model = Worker
        fields = ['id', 'first_name', 'last_name', 'phone_number', 'extra_phone_number', 'birth_date', 'description',
                  'balance', 'currency_type', 'updated_at', 'created_at']

class WorkerSimpleSerializer(ModelSerializer):
    class Meta:
        model = Worker
        fields = ['id', 'first_name', 'last_name', 'phone_number', 'extra_phone_number', 'birth_date', 'description']


class BasketSerializer(ModelSerializer):
    created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    updated_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)

    class Meta:
        model = Basket
        fields = ["id", "name", "size", "weight", "quantity", "price", "per_worker_fee", "updated_at", "created_at"]

class BasketSimpleSerializer(ModelSerializer):
    class Meta:
        model = Basket
        fields = ["id", "name", "size", "weight", "quantity", "price", "per_worker_fee"]


class SupplierSerializer(ModelSerializer):
    created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    updated_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)

    class Meta:
        model = Supplier
        fields = '__all__'

##################################
####### User Daily work ##########
##################################

class UserBasketCountCreateSerializer(ModelSerializer):
    basket = PrimaryKeyRelatedField(queryset=Basket.objects.all())

    class Meta:
        model = UserBasketCount
        fields = ['basket', 'quantity']


class UserDailyWorkCreateSerializer(ModelSerializer):
    worker = PrimaryKeyRelatedField(queryset=Worker.objects.all())
    user_basket_counts = UserBasketCountCreateSerializer(many=True)

    class Meta:
        model = UserDailyWork
        fields = ['worker', 'amount', 'description', 'user_basket_counts']

    def create(self, validated_data):
        with transaction.atomic():
            user_basket_counts_data = validated_data.pop('user_basket_counts')

            user_daily_work = UserDailyWork.objects.create(**validated_data)

            for basket_count_data in user_basket_counts_data:
                UserBasketCount.objects.create(
                    user_daily_work=user_daily_work,
                    **basket_count_data
                )

            user_daily_work.user_basket_counts = UserBasketCount.objects.filter(user_daily_work=user_daily_work)
            return user_daily_work


class UserBasketCountDetailSerializer(ModelSerializer):
    basket = BasketSimpleSerializer()

    class Meta:
        model = UserBasketCount
        fields = ['id', 'basket', 'quantity']

class UserDailyWorkDetailSerializer(ModelSerializer):
    worker = WorkerSimpleSerializer()
    user_basket_counts = UserBasketCountDetailSerializer(many=True, source='userbasketcount_set')

    class Meta:
        model = UserDailyWork
        fields = ['id', 'worker', 'amount', 'description', 'created_at', 'user_basket_counts']


################################

class WorkerGetSerializer(ModelSerializer):
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


class SalaryPaymentGetSerializer(ModelSerializer):
    created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    updated_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    worker=WorkerSerializer()

    class Meta:
        model = SalaryPayment
        fields = ['id','amount','worker','amount','description','currency_type','created_at','updated_at']

class SalaryPaymentPostSerializer(ModelSerializer):
    created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    updated_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)

    class Meta:
        model = SalaryPayment
        fields = ['id', 'amount', 'worker', 'amount', 'description', 'currency_type','created_at','updated_at']
    def create(self, validated_data):
        request = self.context.get('request')

        salary_payment = SalaryPayment.objects.create(**validated_data)

        Expense.objects.create(
            reason="Ishchilarning oylik maoshi",
            description=f"{salary_payment.description} | {salary_payment.id}",
            amount=salary_payment.amount,
            currency_type=salary_payment.currency_type,
            section="factory",
            user=request.user
        )

        return salary_payment