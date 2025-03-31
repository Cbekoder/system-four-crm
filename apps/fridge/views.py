from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import OrderingFilter
from rest_framework.generics import *
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *
from apps.users.permissions import IsFridgeAdmin, IsCEO
from django.utils.dateparse import parse_date
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from datetime import timedelta
from django.db.models import Sum
from django.utils import timezone

from ..main.serializers import TransactionHistorySerializer


# Refrigerator Views
class RefrigatorListCreateView(ListCreateAPIView):
    serializer_class = RefrigeratorSerializer
    queryset = Refrigerator.objects.all()
    permission_classes = [IsFridgeAdmin | IsCEO]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RefrigeratorDetailSerializer
        return RefrigeratorSerializer


class RefrigatorRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = RefrigeratorSerializer
    queryset = Refrigerator.objects.all()
    permission_classes = [IsFridgeAdmin | IsCEO]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RefrigeratorDetailSerializer
        return RefrigeratorSerializer

    def delete(self, request, *args, **kwargs):
        if not request.user.role == 'CEO':
            return Response(
                {"detail": "Only CEO can delete this item."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().delete(request, *args, **kwargs)


# Expense Views
class FridgeExpenseListCreateView(ListCreateAPIView):
    permission_classes = [IsFridgeAdmin | IsCEO]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['created_at', 'price']

    def get_serializer_class(self):
        if self.request.method == "GET":
            return FridgeExpenseSerializer
        return FridgeExpensePostSerializer

    def get_queryset(self):
        queryset = Expense.objects.filter(section='fridge', reason__startswith='expense|')

        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        refrigerator_id = self.request.query_params.get('refrigerator')

        if refrigerator_id:
            queryset = queryset.filter(reason__icontains=f"expense|{refrigerator_id}")

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
                'refrigerator', openapi.IN_QUERY,
                description="Filter by refrigerator ID",
                type=openapi.TYPE_INTEGER
            ),
        ],
        responses={200: FridgeExpenseSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(section="fridge", user=self.request.user)


class FridgeExpenseRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = FridgeExpenseSerializer
    queryset = Expense.objects.all()
    permission_classes = [IsFridgeAdmin | IsCEO]


# Income Views
class FridgeIncomeListCreateView(ListCreateAPIView):
    permission_classes = [IsFridgeAdmin | IsCEO]

    def get_queryset(self):
        queryset = Income.objects.filter(section='fridge')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        refrigerator_id = self.request.query_params.get('refrigerator')

        if refrigerator_id:
            queryset = queryset.filter(reason__icontains=f"income|{refrigerator_id}")

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
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATE
            ),
            openapi.Parameter(
                'end_date', openapi.IN_QUERY,
                description="End date for filtering (YYYY-MM-DD)",
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATE
            ),
            openapi.Parameter(
                'refrigerator', openapi.IN_QUERY,
                description="Filter by refrigerator ID",
                type=openapi.TYPE_INTEGER
            ),
        ],
        responses={200: FridgeIncomeSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return FridgeIncomeSerializer
        return FridgeIncomePostSerializer

    def perform_create(self, serializer):
        serializer.save(section="fridge", user=self.request.user)


class FridgeIncomeRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Income.objects.all()
    serializer_class = FridgeIncomeSerializer
    permission_classes = [IsFridgeAdmin | IsCEO]


# Electricity bill views
class ElectricityBillListCreateView(ListCreateAPIView):
    permission_classes = [IsFridgeAdmin | IsCEO]

    def get_queryset(self):
        queryset = Expense.objects.filter(section='fridge', reason__startswith="electricity|")

        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        refrigerator_id = self.request.query_params.get('refrigerator')

        if refrigerator_id:
            queryset = queryset.filter(reason__icontains=f"electricity|{refrigerator_id}")

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
                'refrigerator', openapi.IN_QUERY,
                description="Filter by refrigerator ID",
                type=openapi.TYPE_INTEGER
            ),
        ],
        responses={200: ElectricityBillSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ElectricityBillSerializer
        return ElectricityBillPostSerializer

    def perform_create(self, serializer):
        serializer.save(section="fridge", user=self.request.user)



class ElectricityBillRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsFridgeAdmin | IsCEO]

    def get_queryset(self):
        queryset = Expense.objects.filter(section='fridge', reason__startswith="electricity|")
        return queryset

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ElectricityBillSerializer
        return ElectricityBillPostSerializer


# Fridge Summary View
class FridgeSummaryAPIView(APIView):
    permission_classes = [IsFridgeAdmin | IsCEO]

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

        expenses = Expense.objects.filter(section='fridge', reason__startswith="expense|",
                                         created_at__range=[start_date, end_date])
        electricity_bills = Expense.objects.filter(section='fridge', reason__startswith="electricity|",
                                                   created_at__range=[start_date, end_date])

        for expense in expenses:
            total_outcome += convert_currency(expense.currency_type, 'UZS', expense.amount)
            outcomes_list.append({
                'id': f"EX-{expense.id}",
                'reason': expense.description,
                'amount': expense.amount,
                'currency_type': expense.currency_type,
                'date': expense.created_at.strftime('%Y-%m-%d')
            })

        for bill in electricity_bills:
            total_outcome += convert_currency(bill.currency_type, "UZS", bill.amount)
            try:
                reason = f"{Refrigerator.objects.get(id=int(bill.reason.split('|')[1])).name} га электр учун тўлов | {bill.description}"
            except Refrigerator.DoesNotExist:
                reason = f"Электр учун тўлов | {bill.description}"
            outcomes_list.append({
                'id': f"EB-{bill.id}",
                'reason': reason,
                'amount': bill.amount,
                'currency_type': bill.currency_type,
                'date': bill.created_at.strftime('%Y-%m-%d')
            })

        # income: Income

        incomes_list = []

        incomes = Income.objects.filter(section='fridge', created_at__range=[start_date, end_date])

        for income in incomes:
            total_income += convert_currency(income.currency_type, "UZS", income.amount)
            try:
                refri_id = income.reason.split('|')
                reason = f"{Refrigerator.objects.get(id=int(income.reason.split('|')[1])).name} дан кирим | {income.description}"
            except Refrigerator.DoesNotExist:
                reason = f"Кирим | {income.description}"
            incomes_list.append({
                'id': f"IN-{income.id}",
                'reason': reason,
                'amount': income.amount,
                'currency_type': income.currency_type,
                'date': income.created_at.strftime('%Y-%m-%d')
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
