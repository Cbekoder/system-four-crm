from datetime import timedelta
from decimal import Decimal

from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.exceptions import ValidationError
from django.utils.dateparse import parse_date
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (
    Driver, Tenant, Contractor, Car, Trailer, CarExpense, SalaryPayment,
    TIR, TIR_STATUS, TIRRecord, Company, Waybill, ContractRecord, ContractIncome, WaybillPayout
)
from .serializers import (
    DriverSerializer, TenantSerializer, ContractorSerializer, CarSerializer, TrailerSerializer,
    CarExpenseSerializer, DriverSalaryPaymentSerializer,
    TIRSerializer, TIRRecordDetailSerializer, TIRRecordSerializer,
    TIRRecordUpdateSerializer, CompanySerializer, WaybillSerializer, ContractRecordDetailSerializer,
    ContractRecordCreateSerializer, ContractIncomeFullDetailSerializer, ContractIncomeCreateSerializer,
    WaybillPayoutDetailSerializer, WaybillPayoutCreateSerializer
)
from apps.users.permissions import IsLogisticAdmin, IsCEO
from apps.main.models import Expense, Income
from ..common.utils import convert_currency
from ..main.serializers import TransactionHistorySerializer


# Driver views
class DriverListCreateView(ListCreateAPIView):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    filter_backends = [SearchFilter]
    search_fields = ['id', 'first_name', 'last_name', 'phone_number', 'description']

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='search',
                in_=openapi.IN_QUERY,
                description='Search across ID, first name, last name, phone number, and description (case-insensitive partial match, exact for ID)',
                type=openapi.TYPE_STRING,
                required=False,
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class DriverRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    permission_classes = [IsLogisticAdmin | IsCEO]


# Tenant views
class TenantListCreateView(ListCreateAPIView):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer
    permission_classes = [IsLogisticAdmin | IsCEO]
    filter_backends = [SearchFilter]
    search_fields = ['first_name', 'last_name', 'phone_number', 'extra_phone_number', 'description', 'trucks_count']

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='search',
                in_=openapi.IN_QUERY,
                description='Search across first name, last name, phone number, extra phone number, description, '
                            'and trucks count (case-insensitive partial match)',
                type=openapi.TYPE_STRING,
                required=False,
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class TenantRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer
    permission_classes = [IsLogisticAdmin | IsCEO]


# Contractor views
class ContractorListCreateView(ListCreateAPIView):
    queryset = Contractor.objects.all()
    serializer_class = ContractorSerializer
    permission_classes = [IsLogisticAdmin | IsCEO]


class ContractorRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Contractor.objects.all()
    serializer_class = ContractorSerializer
    permission_classes = [IsLogisticAdmin | IsCEO]


# Car views
class CarListCreateView(ListCreateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [IsLogisticAdmin | IsCEO]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['tenant']
    search_fields = ['state_number', 'brand', 'model', 'tech_passport']

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='tenant',
                in_=openapi.IN_QUERY,
                description='Filter by tenant ID (exact match)',
                type=openapi.TYPE_INTEGER,
                required=False,
            ),
            openapi.Parameter(
                name='search',
                in_=openapi.IN_QUERY,
                description='Search across state number, brand, model, and tech passport (case-insensitive partial match)',
                type=openapi.TYPE_STRING,
                required=False,
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class CarRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [IsLogisticAdmin | IsCEO]


# Trailer views
class TrailerListCreateView(ListCreateAPIView):
    queryset = Trailer.objects.all()
    serializer_class = TrailerSerializer
    permission_classes = [IsLogisticAdmin | IsCEO]


class TrailerRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Trailer.objects.all()
    serializer_class = TrailerSerializer
    permission_classes = [IsLogisticAdmin | IsCEO]


# TIR views
class TIRListCreateView(ListCreateAPIView):
    queryset = TIR.objects.all()
    serializer_class = TIRSerializer
    permission_classes = [IsLogisticAdmin | IsCEO]
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('status',)
    search_fields = ('serial_number',)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='status',
                in_=openapi.IN_QUERY,
                description='Filter by status',
                type=openapi.TYPE_STRING,
                required=False,
                enum=[status[0] for status in TIR_STATUS],
            ),
            openapi.Parameter(
                name='search',
                in_=openapi.IN_QUERY,
                description='Search by serial number',
                type=openapi.TYPE_STRING,
                required=False,
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = TIR.objects.all()
        status = self.request.query_params.get('status', None)
        if status is not None:
            queryset = queryset.filter(status=status)
        return queryset

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class TIRDetailView(RetrieveUpdateDestroyAPIView):
    queryset = TIR.objects.all()
    serializer_class = TIRSerializer
    permission_classes = [IsLogisticAdmin | IsCEO]


# Company views
class CompanyListCreateView(ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsLogisticAdmin | IsCEO]
    filter_backends = [SearchFilter]
    search_fields = ['name', 'director', 'inn', 'xp', 'mfo', 'phone_number', 'email']

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='search',
                in_=openapi.IN_QUERY,
                description='Search across company name, director name, INN, XP, MFO, phone number, and email (case-insensitive partial match)',
                type=openapi.TYPE_STRING,
                required=False,
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class CompanyDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsLogisticAdmin | IsCEO]


# Waybill views
class WaybillListCreateView(ListCreateAPIView):
    queryset = Waybill.objects.all()
    serializer_class = WaybillSerializer
    permission_classes = [IsLogisticAdmin | IsCEO]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['departure_date', 'car',]
    search_fields = [
        'departure_date', 'arrival_date',
        'driver_1__first_name', 'driver_1__last_name',
        'driver_2__first_name', 'driver_2__last_name',
        'car__state_number', 'trailer__state_number',
        'company__name'
    ]

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
                'car', openapi.IN_QUERY,
                description="Filter by car ID",
                type=openapi.TYPE_INTEGER, required=False
            ),
            openapi.Parameter(
                'search', openapi.IN_QUERY,
                description="Search across departure date, arrival date, driver 1 and 2 first and last names, "
                            "car and trailer state numbers, and company name (case-insensitive partial match)",
                type=openapi.TYPE_STRING,
                required=False
            ),
        ],
        responses={200: WaybillSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

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

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class WaybillDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Waybill.objects.all()
    serializer_class = WaybillSerializer
    permission_classes = [IsLogisticAdmin | IsCEO]


class WaybillPayoutListCreateView(ListCreateAPIView):
    queryset = WaybillPayout.objects.all()
    permission_classes = [IsLogisticAdmin | IsCEO]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['waybill', 'currency_type']
    search_fields = ['waybill__departure_date', 'description', 'currency_type']

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'waybill', openapi.IN_QUERY,
                description="Filter by waybill ID",
                type=openapi.TYPE_INTEGER, required=False
            ),
            openapi.Parameter(
                'currency_type', openapi.IN_QUERY,
                description="Filter by currency type (e.g., USD, UZS)",
                type=openapi.TYPE_STRING, required=False
            ),
            openapi.Parameter(
                'search', openapi.IN_QUERY,
                description="Search across waybill departure date, description, and currency type (case-insensitive partial match)",
                type=openapi.TYPE_STRING, required=False
            ),
        ],
        responses={200: WaybillPayoutDetailSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return WaybillPayoutDetailSerializer
        return WaybillPayoutCreateSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

class WaybillPayoutRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = WaybillPayout.objects.all()
    permission_classes = [IsLogisticAdmin | IsCEO]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return WaybillPayoutDetailSerializer
        return WaybillPayoutCreateSerializer


# TIR Record views
class TIRRecordListCreateView(ListCreateAPIView):
    permission_classes = [IsLogisticAdmin | IsCEO]
    queryset = TIRRecord.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['is_returned']
    search_fields = [
        'tir_get_date', 'tir_deadline', 'is_returned',  # TIRRecord fields
        'tir__serial_number',
        'waybill__driver_1__first_name', 'waybill__driver_1__last_name',  # Driver 1
        'waybill__driver_2__first_name', 'waybill__driver_2__last_name',  # Driver 2
        'waybill__car__state_number', 'waybill__trailer__state_number',  # Car and Trailer
        'waybill__company__name'  # Company
    ]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='is_returned',
                in_=openapi.IN_QUERY,
                description="Filter by returned status (True/False)",
                type=openapi.TYPE_BOOLEAN,
                required=False),
            openapi.Parameter(
                name='search',
                in_=openapi.IN_QUERY,
                description="Search across TIR get date, deadline, returned status, TIR serial number, "
                            "driver 1 and 2 names, car and trailer state numbers, and company name "
                            "(case-insensitive partial match)",
                type=openapi.TYPE_STRING,
                required=False),
        ],
        responses={200: TIRRecordDetailSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TIRRecordDetailSerializer
        return TIRRecordSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class TIRRecordDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsLogisticAdmin | IsCEO]
    queryset = TIRRecord.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TIRRecordDetailSerializer
        return TIRRecordUpdateSerializer


# Contract views
class ContractRecordListCreateView(ListCreateAPIView):
    queryset = ContractRecord.objects.all()
    permission_classes = [IsLogisticAdmin | IsCEO]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ContractRecordDetailSerializer
        return ContractRecordCreateSerializer()

    @swagger_auto_schema(
        request_body=ContractRecordCreateSerializer,
        responses={201: ContractRecordCreateSerializer}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class ContractRecordDetailView(RetrieveUpdateDestroyAPIView):
    queryset = ContractRecord.objects.all()
    permission_classes = [IsLogisticAdmin | IsCEO]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ContractRecordDetailSerializer
        return ContractRecordCreateSerializer


class ContractIncomeListCreateView(ListCreateAPIView):
    queryset = ContractIncome.objects.all()
    permission_classes = [IsLogisticAdmin | IsCEO]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['date', 'contract', 'currency_type']
    search_fields = ['contract__contract_number', 'bank_name', 'currency_type']

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'date', openapi.IN_QUERY,
                description="Filter by payment date (YYYY-MM-DD)",
                type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, required=False
            ),
            openapi.Parameter(
                'contract', openapi.IN_QUERY,
                description="Filter by contract ID",
                type=openapi.TYPE_INTEGER, required=False
            ),
            openapi.Parameter(
                'currency_type', openapi.IN_QUERY,
                description="Filter by currency type (e.g., USD, UZS)",
                type=openapi.TYPE_STRING, required=False
            ),
            openapi.Parameter(
                'search', openapi.IN_QUERY,
                description="Search across contract number, bank name, and currency type (case-insensitive partial match)",
                type=openapi.TYPE_STRING, required=False
            ),
        ],
        responses={200: ContractIncomeFullDetailSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ContractIncomeFullDetailSerializer
        return ContractIncomeCreateSerializer

    def perform_create(self, serializer):
        serializer.save(crator=self.request.user)

class ContractIncomeRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = ContractIncome.objects.all()
    permission_classes = [IsLogisticAdmin | IsCEO]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ContractIncomeFullDetailSerializer
        return ContractIncomeCreateSerializer


# CarExpense views
class CarExpenseListCreateView(ListCreateAPIView):
    queryset = CarExpense.objects.all()
    serializer_class = CarExpenseSerializer
    permission_classes = [IsLogisticAdmin | IsCEO]
    filter_backends = [DjangoFilterBackend, SearchFilter]  # Add SearchFilter
    filterset_fields = ['car', 'trailer']
    search_fields = [
        'car__state_number', 'trailer__state_number',
        'car__brand', 'car__model', 'car__tech_passport',
        'trailer__model', 'trailer__trailer_type', 'trailer__tech_passport'
    ]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='car',
                in_=openapi.IN_QUERY,
                description='Filter by car ID (exact match)',
                type=openapi.TYPE_INTEGER,
                required=False,
            ),
            openapi.Parameter(
                name='trailer',
                in_=openapi.IN_QUERY,
                description='Filter by trailer ID (exact match)',
                type=openapi.TYPE_INTEGER,
                required=False,
            ),
            openapi.Parameter(
                name='search',
                in_=openapi.IN_QUERY,
                description='Search across car state number, brand, model, tech passport, and trailer state number, '
                            'model, type, tech passport (case-insensitive partial match)',
                type=openapi.TYPE_STRING,
                required=False,
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class CarExpenseRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsLogisticAdmin | IsCEO]
    queryset = CarExpense.objects.all()
    serializer_class = CarExpenseSerializer


# SalaryPayment views
class SalaryPaymentListCreateView(ListCreateAPIView):
    permission_classes = [IsLogisticAdmin | IsCEO]
    queryset = SalaryPayment.objects.all()
    serializer_class = DriverSalaryPaymentSerializer
    filter_backends = [SearchFilter]
    search_fields = [
        'id', 'driver__first_name', 'driver__last_name', 'amount', 'description',
        'currency_type', 'driver__middle_name', 'driver__phone_number',
        'driver__licence', 'driver__passport', 'driver__address',
        'driver__extra_phone_number', 'driver__description'
    ]

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
                in_=openapi.IN_QUERY,
                description="Search across ID, driver first name, last name, middle name, phone number, "
                            "extra phone number, licence, passport, address, description, amount, "
                            "and currency type (case-insensitive partial match)",
                type=openapi.TYPE_STRING
            ),
        ],
        responses={200: DriverSalaryPaymentSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class SalaryPaymentRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = SalaryPayment.objects.all()
    serializer_class = DriverSalaryPaymentSerializer
    permission_classes = [IsLogisticAdmin | IsCEO]



class LogisticSummaryAPIView(APIView):
    permission_classes = [IsLogisticAdmin | IsCEO]

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
        responses={200: DriverSalaryPaymentSerializer(many=True)}
    )
    def get(self, request):
        start_date_str = request.query_params.get('start_date', (timezone.now()-timedelta(days=7)).strftime('%Y-%m-%d'))
        end_date_str = request.query_params.get('end_date', timezone.now().strftime('%Y-%m-%d'))

        try:
            start_date = timezone.datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = timezone.datetime.strptime(end_date_str, '%Y-%m-%d')

            # Make the dates timezone-aware (set to the start and end of the day)
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


        # outcome: WaybillPayout, CarExpense, SalaryPayment, Expense

        outcomes_list = []

        waybill_payouts = WaybillPayout.objects.filter(date__range=[start_date, end_date])
        car_expenses = CarExpense.objects.filter(date__range=[start_date, end_date])
        salary_payment = SalaryPayment.objects.filter(date__range=[start_date, end_date])
        expense = Expense.objects.filter(section='logistic', created_at__range=[start_date, end_date])

        for waybill_payout in waybill_payouts:
            total_outcome += waybill_payout.amount
            outcomes_list.append({
                'id': f"WB{waybill_payout.id}",
                'reason': f"{waybill_payout.waybill.id} рақамидаги путёвка учун йўл ҳақи тўлови",
                'amount': waybill_payout.amount,
                'currency_type': waybill_payout.currency_type,
                'date': waybill_payout.date,
            })

        for car_expense in car_expenses:
            total_outcome += car_expense.amount
            reason = ""
            reason += car_expense.car.brand, car_expense.car.state_number, "|" if car_expense.car else ""
            reason += car_expense.trailer.model, car_expense.trailer.state_number if car_expense.trailer else ""
            reason += " учун ҳаражат."
            outcomes_list.append({
                'id': f"CE{car_expense.id}",
                'reason': reason,
                'amount': car_expense.amount,
                'currency_type': car_expense.currency_type,
                'date': car_expense.date,
            })

        for salary_payment in salary_payment:
            total_outcome += salary_payment.amount
            outcomes_list.append({
                'id': f"SP{salary_payment.id}",
                'reason': f"{salary_payment.driver.full_name}га маош учун.",
                'amount': salary_payment.amount,
                'currency_type': salary_payment.currency_type,
                'date': salary_payment.date,
            })

        for expense in expense:
            total_outcome += expense.amount
            outcomes_list.append({
                'id': f"EX{expense.id}",
                'reason': expense.reason,
                'amount': expense.amount,
                'currency_type': expense.currency_type,
                'date': expense.created_at.strftime('%Y-%m-%d'),
            })

        # income: ContractIncome, Income

        incomes_list = []

        contract_income = ContractIncome.objects.filter(date__range=[start_date, end_date])
        income = Income.objects.filter(section='logistic', created_at__range=[start_date, end_date])

        for contract_income in contract_income:
            total_income += contract_income.amount
            incomes_list.append({
                'id': f"CI{contract_income.id}",
                'reason': f"{contract_income.contract.contract_number} рақамли шартнома пули тўланди.",
                'amount': contract_income.amount,
                'currency_type': contract_income.currency_type,
                'date': contract_income.date,
            })

        for income in income:
            total_income += income.amount
            incomes_list.append({
                'id': f"IN{income.id}",
                'reason': income.reason,
                'amount': income.amount,
                'currency_type': income.currency_type,
                'date': income.created_at,
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




        