from datetime import timedelta
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import *
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.users.permissions import IsGardenAdmin, IsCEO
from apps.main.serializers import ExpenseSerializer, IncomeSerializer, TransactionHistorySerializer
from apps.main.models import Income, Expense
from .serializers import *
from django.utils.dateparse import parse_date
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


# Garden Views
class GardenListCreateView(ListCreateAPIView):
    queryset = Garden.objects.all()
    serializer_class = GardenSerializer
    permission_classes = [IsGardenAdmin | IsCEO]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

class GardenRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Garden.objects.all()
    serializer_class = GardenSerializer
    permission_classes = [IsGardenAdmin | IsCEO]


# Gardener Views
class GardenerListCreateView(ListCreateAPIView):
    queryset = Gardener.objects.all()
    serializer_class = GardenerSerializer
    permission_classes = [IsGardenAdmin | IsCEO]

class GardenerRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Gardener.objects.all()
    permission_classes = [IsCEO]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return GardenerDetailSerializer
        return GardenerSerializer


# Gardener Salary Payment Views
class SalaryPaymentListCreateView(ListCreateAPIView):
    queryset = GardenSalaryPayment.objects.all()
    permission_classes = [IsGardenAdmin | IsCEO]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    ordering_fields = ['created_at', 'gardener__balance']
    search_fields = ['gardener__first_name', 'gardener__last_name', 'gardener__phone_number']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GardenerSalaryPaymentGetSerializer
        return GardenerSalaryPaymentSerializer

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
                description="Search by expense columns: id, workers first name and last name, description.",
                type=openapi.TYPE_STRING
            ),
        ],
        responses={200: GardenerSalaryPaymentGetSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class SalaryPaymentRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = GardenSalaryPayment.objects.all()
    serializer_class = GardenerSalaryPaymentSerializer
    permission_classes = [IsGardenAdmin | IsCEO]


# Garden Expense Views
class GardenExpenseListCreateView(ListCreateAPIView):
    permission_classes = [IsGardenAdmin | IsCEO]

    def get_queryset(self):
        queryset = Expense.objects.filter(section="garden")

        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        garden_id = self.request.query_params.get('garden')

        if garden_id:
            try:
                garden = Garden.objects.get(id=garden_id)
                if garden:
                    queryset = queryset.filter(reason__endswith=f"| {garden.id}")
            except ValueError:
                raise ValidationError({"garden": "Invalid garden ID."})

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
                'garden', openapi.IN_QUERY,
                description="Garden ID to filter expenses",
                type=openapi.TYPE_INTEGER
            ),
        ],
        responses={200: ExpenseSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return GardenExpensePostSerializer
        return GardenExpenseSerializer

    def perform_create(self, serializer):
        serializer.save(section="garden",user=self.request.user)

class GardenExpenseRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsGardenAdmin | IsCEO]

    def get_queryset(self):
        queryset = Expense.objects.filter(section="garden")
        return queryset

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GardenExpenseSerializer
        return GardenExpensePostSerializer


# Garden Income Views
class GardenIncomeListCreateView(ListCreateAPIView):
    permission_classes = [IsGardenAdmin | IsCEO]

    def get_queryset(self):
        queryset = Income.objects.filter(section="garden")

        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        garden_id = self.request.query_params.get('garden')

        if garden_id:
            try:
                garden = Garden.objects.get(id=garden_id)
                if garden:
                    queryset = queryset.filter(reason__endswith=f"| {garden.id}")
            except ValueError:
                raise ValidationError({"garden": "Invalid garden ID."})

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
                'garden', openapi.IN_QUERY,
                description="Garden ID to filter incomes",
                type=openapi.TYPE_INTEGER
            ),
        ],
        responses={200: IncomeSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return GardenIncomePostSerializer
        return GardenIncomeSerializer

    def perform_create(self, serializer):
        serializer.save(section="garden", user=self.request.user)

class GardenIncomeRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Income.objects.all()
    permission_classes = [IsGardenAdmin | IsCEO]

    def get_queryset(self):
        queryset = Income.objects.filter(section="garden")
        return queryset

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GardenIncomeSerializer
        return GardenIncomePostSerializer


# Garden Summary
class GardenSummaryAPIView(APIView):
    permission_classes = [IsGardenAdmin | IsCEO]

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
        start_date_str = request.query_params.get('start_date', (timezone.now()-timedelta(days=7)).strftime('%Y-%m-%d'))
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

        # outcome: SalaryPayment, Expense

        outcomes_list = []

        salary_payments = GardenSalaryPayment.objects.filter(created_at__range=[start_date, end_date])
        expense = Expense.objects.filter(section='garden', created_at__range=[start_date, end_date])

        for salary_payment in salary_payments:
            total_outcome += salary_payment.amount
            outcomes_list.append({
                'id': f"SP{salary_payment.id}",
                'reason': f"{salary_payment.gardener.full_name}га маош учун.",
                'amount': salary_payment.amount,
                'currency_type': salary_payment.currency_type,
                'date': salary_payment.created_at.strftime('%Y-%m-%d')
            })

        for expense in expense:
            total_outcome += expense.amount
            outcomes_list.append({
                'id': f"EX{expense.id}",
                'reason': expense.reason,
                'amount': expense.amount,
                'currency_type': expense.currency_type,
                'date': expense.created_at.strftime('%Y-%m-%d')
            })

        # income: Income

        incomes_list = []

        income = Income.objects.filter(section='garden', created_at__range=[start_date, end_date])

        for income in income:
            total_income += income.amount
            incomes_list.append({
                'id': f"IN{income.id}",
                'reason': income.reason,
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