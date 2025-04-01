from datetime import timedelta
from django.db.models import Sum
from django.utils import timezone
from rest_framework import status
from rest_framework.generics import *
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *
from apps.users.permissions import IsFactoryAdmin, IsCEO
from apps.main.models import Expense, Income
from rest_framework.filters import *
from django_filters.rest_framework import DjangoFilterBackend
from apps.main.serializers import ExpenseSerializer, IncomeSerializer, TransactionHistorySerializer
from django.utils.dateparse import parse_date
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Worker Views
class WorkerListCreateView(ListCreateAPIView):
    serializer_class = WorkerSerializer
    queryset = Worker.objects.all()
    permission_classes = [IsFactoryAdmin | IsCEO]
    filter_backends = [DjangoFilterBackend,SearchFilter, OrderingFilter]
    search_fields=['first_name','last_name']
    ordering_fields=['balance']


class WorkerRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = WorkerSerializer
    queryset = Worker.objects.all()
    permission_classes = [IsFactoryAdmin | IsCEO]


# Basket Views
class BasketListCreateView(ListCreateAPIView):
    queryset = Basket.objects.all()
    permission_classes = [IsFactoryAdmin | IsCEO]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return BasketGetSerializer
        return BasketPostSerializer

class BasketRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Basket.objects.all()
    permission_classes = [IsFactoryAdmin | IsCEO]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return BasketGetSerializer
        return BasketPostSerializer



# Daily Work Views
class DailyWorkListCreateView(ListCreateAPIView):
    queryset = UserDailyWork.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    ordering_fields = ['created_at', 'worker']
    search_fields = ['worker__first_name', 'worker__last_name', 'worker__phone_number']
    permission_classes = [IsFactoryAdmin | IsCEO]

    def get_queryset(self):
        queryset = UserDailyWork.objects.all()
        
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        worker_id = self.request.query_params.get('worker')

        if worker_id:
            queryset = queryset.filter(worker__id=worker_id)

        if start_date:
            if not parse_date(start_date):
                raise ValidationError({"start_date": "Invalid date format. Use YYYY-MM-DD."})
            queryset = queryset.filter(created_at__date__gte=start_date)

        if end_date:
            if not parse_date(end_date):
                raise ValidationError({"end_date": "Invalid date format. Use YYYY-MM-DD."})
            queryset = queryset.filter(created_at__date__lte=end_date)

        return queryset

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'start_date', openapi.IN_QUERY,
                description="Start date for filtering (YYYY-MM-DD)",
                type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE
            ),
            openapi.Parameter(
                'end_date', openapi.IN_QUERY,
                description="End date for filtering (YYYY-MM-DD)",
                type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE
            ),
            openapi.Parameter(
                'worker', openapi.IN_QUERY,
                description="Filter by Worker ID",
                type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE
            ),
            openapi.Parameter(
                'search',
                openapi.IN_QUERY,
                description="Search by expense colums: id, worker first name,last name and phone number .",
                type=openapi.TYPE_STRING
            ),
        ],
        responses={200: UserDailyWorkDetailSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserDailyWorkDetailSerializer
        return UserDailyWorkCreateSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class DailyWorkRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = UserDailyWork.objects.all()
    permission_classes = [IsFactoryAdmin | IsCEO]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserDailyWorkDetailSerializer
        return UserDailyWorkCreateSerializer


# Supplier Views
class SupplierListCreateView(ListCreateAPIView):
    serializer_class = SupplierSerializer
    queryset = Supplier.objects.all()
    permission_classes = [IsFactoryAdmin | IsCEO]


class SupplierRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = SupplierSerializer
    queryset = Supplier.objects.all()
    permission_classes = [IsFactoryAdmin | IsCEO]


# Raw Material Views
class RawMaterialListCreateView(ListCreateAPIView):
    serializer_class = RawMaterialSerializer
    queryset = RawMaterial.objects.all()
    permission_classes = [IsFactoryAdmin | IsCEO]

    


class RawMaterialRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = RawMaterialSerializer
    queryset = RawMaterial.objects.all()
    permission_classes = [IsFactoryAdmin | IsCEO]


class RawMaterialHistoryListCreateView(ListCreateAPIView):
    serializer_class = RawMaterialHistorySerializer
    queryset = RawMaterialHistory.objects.all()
    permission_classes = [IsFactoryAdmin | IsCEO]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

class RawMaterialHistoryRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = RawMaterialHistorySerializer
    queryset = RawMaterialHistory.objects.all()
    permission_classes = [IsFactoryAdmin | IsCEO]


    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

# class RawMaterialUsageListCreateView(ListCreateAPIView):
#     serializer_class = RawMaterialUsageSerializer
#     queryset = RawMaterialUsage.objects.all()
#     permission_classes = [IsFactoryAdmin | IsCEO]

    # def perform_create(self, serializer):
    #     serializer.save(creator=self.request.user)

# class RawMaterialUsageRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
#     serializer_class = RawMaterialUsageSerializer
#     queryset = RawMaterialUsage.objects.all()
#     permission_classes = [IsFactoryAdmin | IsCEO]


class FactoryExpenseListCreateView(ListCreateAPIView):
    serializer_class = ExpenseSerializer
    queryset = Expense.objects.all()
    permission_classes = [IsFactoryAdmin | IsCEO]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    ordering_fields = ['created_at', 'amount']
    search_fields=['description','reason']



    def perform_create(self, serializer):
        serializer.save(section="factory", user=self.request.user)


    def get_queryset(self):
        queryset = Expense.objects.filter(section="factory")
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        if start_date:
            if not parse_date(start_date):
                raise ValidationError({"start_date": "Invalid date format. Use YYYY-MM-DD."})
            queryset = queryset.filter(created_at__date__gte=start_date)

        if end_date:
            if not parse_date(end_date):
                raise ValidationError({"end_date": "Invalid date format. Use YYYY-MM-DD."})
            queryset = queryset.filter(created_at__date__lte=end_date)

        return queryset

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'start_date', openapi.IN_QUERY,
                description="Start date for filtering (YYYY-MM-DD)",
                type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE
            ),
            openapi.Parameter(
                'end_date', openapi.IN_QUERY,
                description="End date for filtering (YYYY-MM-DD)",
                type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE
            ),
            openapi.Parameter(
                'search',
                openapi.IN_QUERY,
                description="Search by expense colums: description and reason",
                type=openapi.TYPE_STRING
            ),
        ],
        responses={200: ExpenseSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class FactoryExpenseRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = ExpenseSerializer
    queryset = Expense.objects.all()
    permission_classes = [IsFactoryAdmin | IsCEO]


class FactoryIncomeListCreateView(ListCreateAPIView):
    serializer_class = IncomeSerializer
    queryset = Income.objects.all()
    permission_classes = [IsFactoryAdmin | IsCEO]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    ordering_fields = ['created_at', 'amount']
    search_fields = ['description','reason']

    def get_queryset(self):
        queryset = Income.objects.filter(section="factory")
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        if start_date:
            if not parse_date(start_date):
                raise ValidationError({"start_date": "Invalid date format. Use YYYY-MM-DD."})
            queryset = queryset.filter(created_at__date__gte=start_date)

        if end_date:
            if not parse_date(end_date):
                raise ValidationError({"end_date": "Invalid date format. Use YYYY-MM-DD."})
            queryset = queryset.filter(created_at__date__lte=end_date)

        return queryset

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'start_date', openapi.IN_QUERY,
                description="Start date for filtering (YYYY-MM-DD)",
                type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE
            ),
            openapi.Parameter(
                'end_date', openapi.IN_QUERY,
                description="End date for filtering (YYYY-MM-DD)",
                type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE
            ),
            openapi.Parameter(
                'search',
                openapi.IN_QUERY,
                description="Search by income colums: reason and reason",
                type=openapi.TYPE_STRING
            ),

        ],
        responses={200: IncomeSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(section="factory", user=self.request.user)


class FactoryIncomeRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = IncomeSerializer
    queryset = Income.objects.all()
    permission_classes = [IsFactoryAdmin | IsCEO]


class ClientListCreateView(ListCreateAPIView):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()
    permission_classes = [IsFactoryAdmin | IsCEO]
    filter_backends = [DjangoFilterBackend,  SearchFilter]
    search_fields = ['client__first_name', 'client__last_name', 'client__phone_number']

    def get_queryset(self):
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        if start_date:
            if not parse_date(start_date):
                raise ValidationError({"start_date": "Invalid date format. Use YYYY-MM-DD."})
            self.queryset = self.queryset.filter(created_at__date__gte=start_date)

        if end_date:
            if not parse_date(end_date):
                raise ValidationError({"end_date": "Invalid date format. Use YYYY-MM-DD."})
            self.queryset = self.queryset.filter(created_at__date__lte=end_date)

        return self.queryset

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'start_date', openapi.IN_QUERY,
                description="Start date for filtering (YYYY-MM-DD)",
                type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE
            ),
            openapi.Parameter(
                'end_date', openapi.IN_QUERY,
                description="End date for filtering (YYYY-MM-DD)",
                type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE
            ),
            openapi.Parameter(
                'search',
                openapi.IN_QUERY,
                description="Search by expense columns: id, client's first name,last name and phone number .",
                type=openapi.TYPE_STRING
            ),
        ],
        responses={200: ClientSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)




class ClientRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()
    permission_classes = [IsFactoryAdmin | IsCEO]

# class SaleListCreateView(ListCreateAPIView):
#     serializer_class = SaleSerializer
#     queryset = Sale.objects.all()
#     permission_classes = [IsFactoryAdmin | IsCEO]
#     filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
#     ordering_fields = ['created_at', 'client']
#     search_fields = ['client__first_name', 'client__last_name', 'client__phone_number']
#
#     def get_queryset(self):
#         start_date = self.request.query_params.get('start_date')
#         end_date = self.request.query_params.get('end_date')
#
#         if start_date:
#             if not parse_date(start_date):
#                 raise ValidationError({"start_date": "Invalid date format. Use YYYY-MM-DD."})
#             self.queryset = self.queryset.filter(created_at__date__gte=start_date)
#
#         if end_date:
#             if not parse_date(end_date):
#                 raise ValidationError({"end_date": "Invalid date format. Use YYYY-MM-DD."})
#             self.queryset = self.queryset.filter(created_at__date__lte=end_date)
#
#         return self.queryset

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'start_date', openapi.IN_QUERY,
                description="Start date for filtering (YYYY-MM-DD)",
                type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE
            ),
            openapi.Parameter(
                'end_date', openapi.IN_QUERY,
                description="End date for filtering (YYYY-MM-DD)",
                type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE
            ),
            openapi.Parameter(
                'search',
                openapi.IN_QUERY,
                description="Search by expense columns: id, client's first name,last name and phone number .",
                type=openapi.TYPE_STRING
            ),
        ],
        responses={200: SaleSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)



# class SaleRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
#     serializer_class = SaleSerializer
#     queryset = Sale.objects.all()
#     permission_classes = [IsFactoryAdmin | IsCEO]



class SalaryPaymentListCreateView(ListCreateAPIView):
    queryset = SalaryPayment.objects.all()
    permission_classes = [IsFactoryAdmin | IsCEO]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    ordering_fields = ['worker', 'worker__balance','amount']
    searching_fields=['worker__first_name','worker__last_name','worker__phone_number']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SalaryPaymentGetSerializer
        return SalaryPaymentPostSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def get_queryset(self):
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        if start_date:
            if not parse_date(start_date):
                raise ValidationError({"start_date": "Invalid date format. Use YYYY-MM-DD."})
            self.queryset = self.queryset.filter(created_at__date__gte=start_date)

        if end_date:
            if not parse_date(end_date):
                raise ValidationError({"end_date": "Invalid date format. Use YYYY-MM-DD."})
            self.queryset = self.queryset.filter(created_at__date__lte=end_date)

        return self.queryset

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'start_date', openapi.IN_QUERY,
                description="Start date for filtering (YYYY-MM-DD)",
                type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE
            ),
            openapi.Parameter(
                'end_date', openapi.IN_QUERY,
                description="End date for filtering (YYYY-MM-DD)",
                type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE
            ),
            openapi.Parameter(
                'search',
                openapi.IN_QUERY,
                description="Search by salary payment columns: id, worker's first name,last name and phone number .",
                type=openapi.TYPE_STRING
            ),
        ],
        responses={200: SalaryPaymentGetSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class SalaryPaymentRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = SalaryPaymentGetSerializer
    queryset = SalaryPayment.objects.all()
    permission_classes = [IsFactoryAdmin | IsCEO]

    def get_serializer_class(self):
        if self.request.method == 'PUT' or self.request.method=='PATCH':
            return SalaryPaymentPostSerializer
        return SalaryPaymentGetSerializer


class SaleListCreateView(ListCreateAPIView):
    queryset = Sale.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SaleGetSerializer
        return SaleSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

# Bitta sotuvni olish, yangilash va o‘chirish (GET, PUT, DELETE)
class SaleRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer

# SaleItem uchun CRUD
class SaleItemListCreateView(ListCreateAPIView):
    queryset = SaleItem.objects.all()
    serializer_class = SaleItemSerializer

class SaleItemRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = SaleItem.objects.all()
    serializer_class = SaleItemSerializer



class FactorySummaryAPIView(APIView):
    permission_classes = [IsFactoryAdmin | IsCEO]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'start_date', openapi.IN_QUERY,
                description="Start date for filtering (YYYY-MM-DD)",
                type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE
            ),
            openapi.Parameter(
                'end_date', openapi.IN_QUERY,
                description="End date for filtering (YYYY-MM-DD)",
                type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE
            )
        ],
        responses={
            200: openapi.Response(
                description="Financial overview",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'start_date': openapi.Schema(type=openapi.TYPE_STRING, description="Start date in YYYY-MM-DD"),
                        'end_date': openapi.Schema(type=openapi.TYPE_STRING, description="End date in YYYY-MM-DD"),
                        'balance': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'uzs': openapi.Schema(type=openapi.TYPE_NUMBER, description="Balance in UZS"),
                                'usd': openapi.Schema(type=openapi.TYPE_NUMBER, description="Balance in USD"),
                                'rub': openapi.Schema(type=openapi.TYPE_NUMBER, description="Balance in RUB"),
                            }
                        ),
                        'total_income': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'uzs': openapi.Schema(type=openapi.TYPE_NUMBER, description="Total income in UZS"),
                                'usd': openapi.Schema(type=openapi.TYPE_NUMBER, description="Total income in USD"),
                                'rub': openapi.Schema(type=openapi.TYPE_NUMBER, description="Total income in RUB"),
                            }
                        ),
                        'total_outcome': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'uzs': openapi.Schema(type=openapi.TYPE_NUMBER, description="Total outcome in UZS"),
                                'usd': openapi.Schema(type=openapi.TYPE_NUMBER, description="Total outcome in USD"),
                                'rub': openapi.Schema(type=openapi.TYPE_NUMBER, description="Total outcome in RUB"),
                            }
                        ),
                        'incomes': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                description="Transaction history object",
                            ),
                            description="List of income transactions"
                        ),
                        'outcomes': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                description="Transaction history object",
                            ),
                            description="List of outcome transactions"
                        ),
                    },
                    required=['start_date', 'end_date', 'balance', 'total_income', 'total_outcome', 'incomes',
                              'outcomes']
                )
            )
        }
    )
    def get(self, request):
        start_date_str = request.query_params.get('start_date',
                                                  (timezone.now() - timedelta(days=7)).strftime('%Y-%m-%d'))
        end_date_str = request.query_params.get('end_date', timezone.now().strftime('%Y-%m-%d'))

        try:
            start_date = timezone.datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = timezone.datetime.strptime(end_date_str, '%Y-%m-%d')

            start_date = timezone.make_aware(
                timezone.datetime(start_date.year, start_date.month, start_date.day, 0, 0, 0)
            )
            end_date = timezone.make_aware(
                timezone.datetime(end_date.year, end_date.month, end_date.day, 23, 59, 59)
            )
        except ValueError:
            return Response(
                {"error": "Invalid date format. Use YYYY-MM-DD."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if end_date < start_date:
            return Response(
                {"error": "end_date cannot be before start_date."},
                status=status.HTTP_400_BAD_REQUEST
            )

        total_income = 0.00
        total_outcome = 0.00

        # outcome: Expense

        outcomes_list = []

        expenses = Expense.objects.filter(section='factory', created_at__range=[start_date, end_date])
        salaries = SalaryPayment.objects.filter(created_at__range=[start_date, end_date])
        raw_material = RawMaterialHistory.objects.filter(date__range=[start_date, end_date])


        for expense in expenses:
            total_outcome += convert_currency(expense.currency_type, 'UZS', expense.amount)
            outcomes_list.append({
                'id': f"EX-{expense.id}",
                'reason': f"{expense.reason} | {expense.description}",
                'amount': expense.amount,
                'currency_type': expense.currency_type,
                'date': expense.created_at.strftime('%Y-%m-%d')
            })

        for salary in salaries:
            total_outcome += convert_currency(salary.currency_type, 'UZS', salary.amount)
            outcomes_list.append({
                'id': f"SP-{salary.id}",
                'reason': f"{salary.worker.full_name} га маош учун | {salary.description}",
                'amount': salary.amount,
                'currency_type': salary.currency_type,
                'date': salary.created_at.strftime('%Y-%m-%d')
            })

        for raw in raw_material:
            total_outcome += convert_currency(raw.currency_type, 'UZS', raw.amount)
            outcomes_list.append({
                'id': f"RM-{raw.id}",
                'reason': f"{raw.weight} кг {raw.raw_material.name} учун | {raw.description}",
                'amount': raw.amount,
                'currency_type': raw.currency_type,
                'date': raw.created_at.strftime('%Y-%m-%d')
            })

        # income: Income

        incomes_list = []

        incomes = Income.objects.filter(section='factory', created_at__range=[start_date, end_date])
        sales = Sale.objects.filter(date__range=[start_date, end_date], is_debt=False)

        for income in incomes:
            total_income += convert_currency(income.currency_type, 'UZS', income.amount)
            incomes_list.append({
                'id': f"IN-{income.id}",
                'reason': income.reason,
                'amount': income.amount,
                'currency_type': income.currency_type,
                'date': income.created_at.strftime('%Y-%m-%d')
            })

        for sale in sales:
            total_income += sale.total_amount
            incomes_list.append({
                'id': f"SA-{sale.id}",
                'reason': f"{sale.client.full_name if sale.client else 'Номаълум мижоз'} га сотув учун",
                'amount': sale.total_amount,
                'currency_type': "UZS",
                'date': sale.date.strftime('%Y-%m-%d')
            })

        return Response({
            'start_date': start_date_str,
            'end_date': end_date_str,
            'balance': {
                'uzs': convert_currency(request.user.currency_type, "UZS", request.user.balance),
                'usd': convert_currency(request.user.currency_type, "USD", request.user.balance),
                'rub': convert_currency(request.user.currency_type, "RUB", request.user.balance)
            },
            'total_income': {
                'uzs': total_income,
                'usd': convert_currency("UZS", "USD", total_income),
                'rub': convert_currency("UZS", "RUB", total_income)
            },
            'total_outcome': {
                'uzs': total_outcome,
                'usd': convert_currency("UZS", "USD", total_outcome),
                'rub': convert_currency("UZS", "RUB", total_outcome)
            },
            'incomes': TransactionHistorySerializer(incomes_list, many=True).data,
            'outcomes': TransactionHistorySerializer(outcomes_list, many=True).data,
        })


