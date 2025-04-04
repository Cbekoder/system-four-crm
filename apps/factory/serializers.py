from django.utils import timezone
from rest_framework.relations import StringRelatedField
from rest_framework.serializers import ModelSerializer, ValidationError, CharField, DateTimeField, \
    PrimaryKeyRelatedField, SerializerMethodField
from .models import *
from apps.main.models import Expense, Income


# Worker Serializers
class WorkerSerializer(ModelSerializer):
    created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    updated_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)

    class Meta:
        model = Worker
        fields = ['id', 'first_name', 'last_name', 'phone_number', 'extra_phone_number', 'birth_date', 'description',
                  'balance', 'currency_type', 'updated_at', 'created_at']
        read_only_fields = ['balance', 'created_at', 'updated_at']

class WorkerSimpleSerializer(ModelSerializer):
    class Meta:
        model = Worker
        fields = ['id', 'first_name', 'last_name']


# Basket Serializers
class BasketPostSerializer(ModelSerializer):
    class Meta:
        model = Basket
        fields = ["id", "name", "size", "weight", "quantity", "price", "per_worker_fee", "raw_material"]

class BasketGetSerializer(ModelSerializer):
    created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    updated_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    raw_material = StringRelatedField()
    class Meta:
        model = Basket
        fields = ["id", "name", "size", "weight", "quantity", "price", "per_worker_fee", "raw_material", "updated_at", "created_at"]


class BasketSimpleSerializer(ModelSerializer):
    class Meta:
        model = Basket
        fields = ["id", "name", "size", "weight", "quantity", "price", "per_worker_fee"]


# Supplier Serializers
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
        fields = ['id', 'worker', 'amount', 'description', 'date', 'user_basket_counts', 'updated_at', 'created_at']
        read_only_fields = ['id', 'amount']

    def create(self, validated_data):
        with transaction.atomic():
            user_basket_counts_data = validated_data.pop('user_basket_counts')

            if validated_data.get('date') is None:
                validated_data['date'] = timezone.now().date()

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


# Sale Serializers
class SaleItemSerializer(ModelSerializer):
    # basket = BasketSerializer(read_only=True)
    # basket_id = PrimaryKeyRelatedField(
    #     queryset=Basket.objects.all(), source='basket', write_only=True
    # )

    class Meta:
        model = SaleItem
        fields = ['id', 'basket', 'quantity','amount']



class SaleSerializer(ModelSerializer):
    sale_items = SaleItemSerializer(many=True)

    class Meta:
        model = Sale
        fields = ['id', 'client', 'description', 'total_amount', 'date' ,'sale_items','payed_amount']

    def create(self, validated_data):
        with transaction.atomic():
            sale_items_data = validated_data.pop('sale_items')
            sale = Sale.objects.create(**validated_data)

            for item_data in sale_items_data:
                SaleItem.objects.create(sale=sale, **item_data)

            return sale


    def update(self, instance, validated_data):
        sale_items_data = validated_data.pop('sale_items', [])


        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()


        existing_items = {item.basket_id: item for item in instance.sale_items.all()}


        new_basket_ids = []

        for item_data in sale_items_data:
            basket_id = item_data['basket'].id if isinstance(item_data['basket'], Basket) else item_data['basket']
            new_basket_ids.append(basket_id)

            if basket_id in existing_items:
                # Mavjud bo‘lsa, yangilaymiz
                item = existing_items[basket_id]
                item.quantity = item_data['quantity']
                item.amount = item_data['amount']
                item.save()
            else:

                SaleItem.objects.create(sale=instance, **item_data)


        for basket_id, item in existing_items.items():
            if basket_id not in new_basket_ids:
                item.delete()

        return instance


class SaleGetSerializer(ModelSerializer):
    created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    updated_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    sale_items = SaleItemSerializer(many=True)
    client = SerializerMethodField()

    class Meta:
        model = Sale
        fields = ['id', 'client', 'description', 'total_amount', 'date', 'total_quantity','sale_items','payed_amount','debt_amount','created_at', 'updated_at']

    def get_client(self, obj):
        if obj.client:
            return {
                "first_name": obj.client.first_name,
                "last_name": obj.client.last_name,
                "debt": obj.client.debt
            }
        return None


# Raw Material History Serializers
class RawMaterialHistorySerializer(ModelSerializer):
    created_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)
    updated_at = DateTimeField(format="%d.%m.%Y %H:%M", read_only=True)

    class Meta:
        model = RawMaterialHistory
        fields = ['id', 'supplier', 'raw_material', 'date' ,'amount', 'weight', 'currency_type', 'created_at', 'updated_at']


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
        fields = ['id',  'amount',  'worker',  'amount',  'date', 'description',  'currency_type', 'created_at', 'updated_at']

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


# Pay Debts Serializer
class PayDebtPostSerializer(ModelSerializer):
    class Meta:
        model = PayDebt
        fields = ['id', 'client', 'amount', 'currency_type', 'description', 'date']

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class PayDebtGetSerializer(ModelSerializer):
    client = ClientSerializer()
    class Meta:
        model = PayDebt
        fields = ['id', 'client', 'amount', 'currency_type', 'description', 'date']


