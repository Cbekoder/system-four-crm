from rest_framework.filters import SearchFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.exceptions import ValidationError
from django.utils.dateparse import parse_date
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import (
    Driver, Tenant, Contractor, Car, Trailer, CarExpense, SalaryPayment,
    Contract, Transit, TransitExpense, TransitIncome
)
from .serializers import (
    DriverSerializer, TenantSerializer, ContractorSerializer, CarSerializer, TrailerSerializer,
    CarExpenseSerializer, DriverSalaryPaymentSerializer, ContractSerializer, TransitGetSerializer,
    TransitPostSerializer, TransitDetailSerializer,
    TransitExpenseSerializer, TransitIncomeSerializer
)
from apps.users.models import User
from apps.users.serializers import UserDetailSerializer, UserPostSerializer
from apps.users.permissions import IsCEOOrAdmin, IsAdmin, IsCEO


# Generic Views for Driver
class DriverListCreateView(ListCreateAPIView):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    filter_backends = [SearchFilter]
    permission_classes = [IsCEOOrAdmin]
    search_fields = ['id', 'first_name', 'last_name', 'phone_number', 'description']

    # def get_permissions(self):
    #     if self.request.method == 'GET':
    #         permission_classes = [IsCEO | IsAdmin]
    #     else:
    #         permission_classes = [IsCEO | IsAdmin]
    #     return [permission() for permission in permission_classes]


class DriverRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer


# Generic Views for Tenant
class TenantListCreateView(ListCreateAPIView):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer


class TenantRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer


# Generic Views for Contractor
class ContractorListCreateView(ListCreateAPIView):
    queryset = Contractor.objects.all()
    serializer_class = ContractorSerializer


class ContractorRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Contractor.objects.all()
    serializer_class = ContractorSerializer


# Generic Views for Car
class CarListCreateView(ListCreateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer


class CarRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer


# Generic Views for Trailer
class TrailerListCreateView(ListCreateAPIView):
    queryset = Trailer.objects.all()
    serializer_class = TrailerSerializer


class TrailerRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Trailer.objects.all()
    serializer_class = TrailerSerializer


# Generic Views for CarExpense
class CarExpenseListCreateView(ListCreateAPIView):
    queryset = CarExpense.objects.all()
    serializer_class = CarExpenseSerializer


class CarExpenseRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = CarExpense.objects.all()
    serializer_class = CarExpenseSerializer


# Generic Views for SalaryPayment
class SalaryPaymentListCreateView(ListCreateAPIView):
    queryset = SalaryPayment.objects.all()
    serializer_class = DriverSalaryPaymentSerializer
    filter_backends = [SearchFilter]
    search_fields = ['id', 'driver__first_name', 'driver__last_name', 'amount', 'description']

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
                description="Search by expense colums: id, driver first name and last name, description.",
                type=openapi.TYPE_STRING
            ),
        ],
        responses={200: DriverSalaryPaymentSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class SalaryPaymentRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = SalaryPayment.objects.all()
    serializer_class = DriverSalaryPaymentSerializer


# Generic Views for Contract
class ContractListCreateView(ListCreateAPIView):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    filter_backends = [SearchFilter]
    search_fields = ['id', 'contractor__first_name', 'contractor__last_name', 'contract_id']

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
            # openapi.Parameter(
            #     'search',
            #     openapi.IN_QUERY,
            #     description="Search by expense colums: id, driver first name and last name, description.",
            #     type=openapi.TYPE_STRING
            # ),
        ],
        responses={200: ContractSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ContractRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer


# Generic Views for Transit
class TransitListCreateView(ListCreateAPIView):
    queryset = Transit.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TransitGetSerializer
        return TransitPostSerializer

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
            # openapi.Parameter(
            #     'search',
            #     openapi.IN_QUERY,
            #     description="Search by expense colums: id, driver first name and last name, description.",
            #     type=openapi.TYPE_STRING
            # ),
        ],
        responses={200: TransitGetSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class TransitRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Transit.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TransitDetailSerializer
        return TransitPostSerializer


# Generic Views for TransitExpense
class TransitExpenseListCreateView(ListCreateAPIView):
    queryset = TransitExpense.objects.all()
    serializer_class = TransitExpenseSerializer

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
        ],
        responses={200: TransitExpenseSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class TransitExpenseRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = TransitExpense.objects.all()
    serializer_class = TransitExpenseSerializer


# Generic Views for TransitIncome
class TransitIncomeListCreateView(ListCreateAPIView):
    queryset = TransitIncome.objects.all()
    serializer_class = TransitIncomeSerializer

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
        ],
        responses={200: TransitIncomeSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class TransitIncomeRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = TransitIncome.objects.all()
    serializer_class = TransitIncomeSerializer


# Admin user views
class LogisticUserListCreateAPIView(ListCreateAPIView):
    permission_classes = [IsCEO]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserDetailSerializer
        return UserPostSerializer

    def get_queryset(self):
        queryset = User.objects.filter(section="logistic")
        return queryset

    def perform_create(self, serializer):
        serializer.save(section="logistic")


class LogisticUserRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserDetailSerializer

    def get_queryset(self):
        queryset = User.objects.filter(section="logistic")
        return queryset

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserDetailSerializer
        return UserPostSerializer
