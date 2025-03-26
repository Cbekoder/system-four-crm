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
        fields = ['id', 'first_name', 'last_name']


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
        fields = ['id', 'name', 'phone_number', 'extra_phone_number', 'description', 'created_at', 'updated_at']

##################################
####### User Daily work ##########
##################################

class UserBasketCountCreateSerializer(ModelSerializer):
    basket = PrimaryKeyRelatedField(queryset=Basket.objects.all())

    class Meta:
        model = UserBasketCount
        fields = ['id', 'basket', 'quantity']


class UserDailyWorkCreateSerializer(ModelSerializer):
    worker = PrimaryKeyRelatedField(queryset=Worker.objects.all())
    user_basket_counts = UserBasketCountCreateSerializer(many=True)
    created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    updated_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)

    class Meta:
        model = UserDailyWork
        fields = ['id', 'worker', 'amount', 'description',  'user_basket_counts','date', 'updated_at', 'created_at']
        read_only_fields = ['id', 'amount']

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

    def update(self, instance, validated_data):
        with transaction.atomic():
            instance.worker = validated_data.get('worker', instance.worker)
            instance.description = validated_data.get('description', instance.description)
            instance.save()

            if 'user_basket_counts' in validated_data:
                user_basket_counts_data = validated_data.pop('user_basket_counts')
                existing_basket_counts = {bc.id: bc for bc in instance.userbasketcount_set.all()}
                incoming_ids = {item.get('id') for item in user_basket_counts_data if 'id' in item}

                for bc_id, bc_instance in existing_basket_counts.items():
                    if bc_id not in incoming_ids:
                        bc_instance.delete()

                for basket_count_data in user_basket_counts_data:
                    basket_count_id = basket_count_data.get('id', None)
                    if basket_count_id and basket_count_id in existing_basket_counts:
                        bc_instance = existing_basket_counts[basket_count_id]
                        bc_instance.basket = basket_count_data.get('basket', bc_instance.basket)
                        bc_instance.quantity = basket_count_data.get('quantity', bc_instance.quantity)
                        bc_instance.save()
                    else:
                        UserBasketCount.objects.create(
                            user_daily_work=instance,
                            **basket_count_data
                        )
            instance.user_basket_counts = UserBasketCount.objects.filter(user_daily_work=instance)

            return instance


class UserBasketCountDetailSerializer(ModelSerializer):
    basket = BasketSimpleSerializer()

    class Meta:
        model = UserBasketCount
        fields = ['id', 'basket', 'quantity']

class UserDailyWorkDetailSerializer(ModelSerializer):
    worker = WorkerSimpleSerializer()
    user_basket_counts = UserBasketCountDetailSerializer(many=True, source='userbasketcount_set')
    created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    updated_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)

    class Meta:
        model = UserDailyWork
        fields = ['id', 'worker', 'amount', 'description', 'date', 'updated_at', 'created_at', 'user_basket_counts']


################################

class WorkerGetSerializer(ModelSerializer):
    created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    updated_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)

    class Meta:
        model = Worker
        fields = ['id', 'first_name', 'last_name', 'phone_number', 'debt', 'currency_type', 'created_at', 'updated_at']


class RawMaterialSerializer(ModelSerializer):
    # created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    # updated_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)

    class Meta:
        model = RawMaterial
        fields = ['id', 'name', 'description', 'weight']

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
    # created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    # updated_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)

    class Meta:
        model = Client
        fields = ['id', 'first_name','last_name','phone_number','debt','currency_type']


# class SaleSerializer(ModelSerializer):
#     created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
#     updated_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
#
#     class Meta:
#         model = Sale
#         fields = '__all__'

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


class SaleItemSerializer(ModelSerializer):
    # basket = BasketSerializer(read_only=True)
    # basket_id = PrimaryKeyRelatedField(
    #     queryset=Basket.objects.all(), source='basket', write_only=True
    # )

    class Meta:
        model = SaleItem
        fields = ['id', 'basket', 'quantity','amount']

    # def create(self, validated_data):
    #     request = self.context.get('request')
    #
    #     sale_items_data = validated_data.pop('sale_items', [])
    #     sale = Sale.objects.create(**validated_data)
    #
    #     for item_data in sale_items_data:
    #         SaleItem.objects.create(sale=sale, **item_data)
    #
    #     # Daromadni yaratish
    #     Income.objects.create(
    #         reason=f"Korzinka sotuvi | {sale.client.first_name} {sale.client.last_name if sale.client else ''}",
    #         description=sale.description,
    #         amount=sale.amount,
    #         currency_type=sale.currency_type,
    #         section="factory",
    #         user=request.user if request else None
    #     )
    #
    #     return sale


class SaleSerializer(ModelSerializer):
    sale_items = SaleItemSerializer(many=True)

    class Meta:
        model = Sale
        fields = ['id', 'client', 'description', 'is_debt', 'total_amount','date' ,'sale_items']

    def create(self, validated_data):
        sale_items_data = validated_data.pop('sale_items')
        sale = Sale.objects.create(**validated_data)

        for item_data in sale_items_data:
            SaleItem.objects.create(sale=sale, **item_data)

        return sale


    def update(self, instance, validated_data):
        sale_items_data = validated_data.pop('sale_items', [])

        # Mavjud ma'lumotlarni yangilash
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Yangi sale_items qo'shish
        for item_data in sale_items_data:
            SaleItem.objects.create(sale=instance, **item_data)

        return instance

class SaleGetSerializer(ModelSerializer):
    created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    updated_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    sale_items = SaleItemSerializer(many=True)
    client = SerializerMethodField()

    class Meta:
        model = Sale
        fields = ['id', 'client', 'description', 'is_debt', 'total_amount', 'date', 'total_quantity','sale_items','created_at', 'updated_at']

    def get_client(self, obj):
        if obj.client:
            return {
                "first_name": obj.client.first_name,
                "last_name": obj.client.last_name,
                "debt": obj.client.debt
            }
        return None

class RawMaterialHistorySerializer(ModelSerializer):
    created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    updated_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)

    class Meta:
        model = RawMaterialHistory
        fields = ['id', 'supplier', 'raw_material','date' ,'amount', 'weight', 'currency_type', 'created_at', 'updated_at']


class SalaryPaymentGetSerializer(ModelSerializer):
    created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    updated_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    worker=WorkerSerializer()

    class Meta:
        model = SalaryPayment
        fields = ['id', 'amount', 'worker', 'amount', 'description', 'currency_type', 'created_at', 'updated_at']

class SalaryPaymentPostSerializer(ModelSerializer):
    created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    updated_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)

    class Meta:
        model = SalaryPayment
        fields = ['id',  'amount',  'worker',  'amount',  'description',  'currency_type', 'created_at', 'updated_at']

    # def create(self, validated_data):
    #     request = self.context.get('request')
    #
    #     salary_payment = SalaryPayment.objects.create(**validated_data)
    #
    #     Expense.objects.create(
    #         reason="Ishchilarning oylik maoshi",
    #         description=f"{salary_payment.description} | {salary_payment.id}",
    #         amount=salary_payment.amount,
    #         currency_type=salary_payment.currency_type,
    #         section="factory",
    #         user=request.user
    #     )
    #     return salary_payment

# class RawMaterialUsageSerializer(ModelSerializer):
#     class Meta:
#         model = RawMaterialUsage
#         fields = ['id', 'raw_material', 'amount', 'date']


#Serializers for summary


class SaleSummarySerializer(ModelSerializer):
    amount = CharField(source='total_amount')
    reason = SerializerMethodField()

    class Meta:
        model = Sale
        fields = ['id', 'description', 'reason', 'amount', 'date']

    def get_reason(self, obj):
        return f"{obj.client.first_name} {obj.client.last_name}ga {obj.total_quantity} ta savat sotildi"


class RawMaterialHistorySummarySerializer(ModelSerializer):
    reason=SerializerMethodField()
    class Meta:
        model = RawMaterialHistory
        fields = ['id','description','reason', 'amount', 'date']

    def get_reason(self, obj):
        return f"{obj.raw_material.name} xomashyosi otib olindi"

class DailyWorkSummarySerializer(ModelSerializer):
    class Meta:
        model = UserDailyWork
        fields = ['id', 'description','reason', 'amount', 'date']

class SalaryPaymentSummarySerializer(ModelSerializer):
    reason=SerializerMethodField()
    class Meta:
        model = SalaryPayment
        fields = ['id', 'description', 'reason','amount', 'date']

    def get_reason(self,obj):
        return f"{obj.worker.first_name} {obj.worker.last_name}ga {obj.amount} miqdorda maosh berildi"

class ExpenseSummarySerializer(ModelSerializer):
    date=DateTimeField(format="%d.%m.%Y", source='created_at')
    class Meta:
        model = Expense
        fields = ['id', 'description', 'reason','amount', 'date']

class IncomeSummarySerializer(ModelSerializer):
    date=DateTimeField(format="%d.%m.%Y", source='created_at')
    class Meta:
        model = Income
        fields = ['id', 'description', 'reason','amount', 'date']
