from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.exceptions import ValidationError
from django.utils.dateparse import parse_date
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import (
    Driver, Tenant, Contractor, Car, Trailer, CarExpense, SalaryPayment,
    TIR, TIR_STATUS, TIRRecord, Company, Waybill, ContractRecord,
    # Contract, Transit, TransitExpense, TransitIncome,
)
from .serializers import (
    DriverSerializer, TenantSerializer, ContractorSerializer, CarSerializer, TrailerSerializer,
    CarExpenseSerializer, DriverSalaryPaymentSerializer,
    TIRSerializer, TIRRecordDetailSerializer, TIRRecordSerializer,
    TIRRecordUpdateSerializer, CompanySerializer, WaybillSerializer, ContractRecordDetailSerializer, ContractRecordCreateSerializer
)
from apps.users.permissions import IsLogisticAdmin, IsCEO


# Driver views
class DriverListCreateView(ListCreateAPIView):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    filter_backends = [SearchFilter]
    search_fields = ['id', 'first_name', 'last_name', 'phone_number', 'description']


class DriverRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    permission_classes = [IsLogisticAdmin, IsCEO]


# Tenant views
class TenantListCreateView(ListCreateAPIView):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer
    permission_classes = [IsLogisticAdmin, IsCEO]


class TenantRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer
    permission_classes = [IsLogisticAdmin, IsCEO]


# Generic Views for Contractor
class ContractorListCreateView(ListCreateAPIView):
    queryset = Contractor.objects.all()
    serializer_class = ContractorSerializer
    permission_classes = [IsLogisticAdmin, IsCEO]


class ContractorRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Contractor.objects.all()
    serializer_class = ContractorSerializer
    permission_classes = [IsLogisticAdmin, IsCEO]


# Generic Views for Car
class CarListCreateView(ListCreateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [IsLogisticAdmin, IsCEO]


class CarRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [IsLogisticAdmin, IsCEO]


# Generic Views for Trailer
class TrailerListCreateView(ListCreateAPIView):
    queryset = Trailer.objects.all()
    serializer_class = TrailerSerializer
    permission_classes = [IsLogisticAdmin, IsCEO]



class TrailerRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Trailer.objects.all()
    serializer_class = TrailerSerializer
    permission_classes = [IsLogisticAdmin, IsCEO]


class TIRListCreateView(ListCreateAPIView):
    queryset = TIR.objects.all()
    serializer_class = TIRSerializer
    permission_classes = [IsLogisticAdmin, IsCEO]
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('status',)

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
    permission_classes = [IsLogisticAdmin, IsCEO]


class CompanyListCreateView(ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsLogisticAdmin, IsCEO]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

class CompanyDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsLogisticAdmin, IsCEO]


class WaybillListCreateView(ListCreateAPIView):
    queryset = Waybill.objects.all()
    serializer_class = WaybillSerializer
    permission_classes = [IsLogisticAdmin, IsCEO]

class WaybillDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Waybill.objects.all()
    serializer_class = WaybillSerializer
    permission_classes = [IsLogisticAdmin, IsCEO]


class TIRRecordListCreateView(ListCreateAPIView):
    permission_classes = [IsLogisticAdmin, IsCEO]
    queryset = TIRRecord.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TIRRecordDetailSerializer
        return TIRRecordSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class TIRRecordDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsLogisticAdmin, IsCEO]
    queryset = TIRRecord.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TIRRecordDetailSerializer
        return TIRRecordUpdateSerializer


class ContractRecordListCreateView(ListCreateAPIView):
    queryset = ContractRecord.objects.all()
    permission_classes = [IsLogisticAdmin, IsCEO]

    def perform_create(self, serializer):
        """Optional: Additional logic before saving."""
        serializer.save(creator=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ContractRecordDetailSerializer
        return ContractRecordCreateSerializer

class ContractRecordDetailView(RetrieveUpdateDestroyAPIView):
    queryset = ContractRecord.objects.all()
    permission_classes = [IsLogisticAdmin, IsCEO]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ContractRecordDetailSerializer
        return ContractRecordCreateSerializer


# Generic Views for CarExpense
class CarExpenseListCreateView(ListCreateAPIView):
    queryset = CarExpense.objects.all()
    serializer_class = CarExpenseSerializer
    permission_classes = [IsLogisticAdmin, IsCEO]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class CarExpenseRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsLogisticAdmin, IsCEO]
    queryset = CarExpense.objects.all()
    serializer_class = CarExpenseSerializer


# Generic Views for SalaryPayment
class SalaryPaymentListCreateView(ListCreateAPIView):
    permission_classes = [IsLogisticAdmin, IsCEO]
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

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class SalaryPaymentRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = SalaryPayment.objects.all()
    serializer_class = DriverSalaryPaymentSerializer
    permission_classes = [IsLogisticAdmin, IsCEO]


# Generic Views for Contract
# class ContractListCreateView(ListCreateAPIView):
#     queryset = Contract.objects.all()
#     serializer_class = ContractSerializer
#     filter_backends = [SearchFilter]
#     search_fields = ['id', 'contractor__first_name', 'contractor__last_name', 'contract_id']
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
#
#     @swagger_auto_schema(
#         manual_parameters=[
#             openapi.Parameter(
#                 'start_date', openapi.IN_QUERY,
#                 description="Start date for filtering (YYYY-MM-DD)",
#                 type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE
#             ),
#             openapi.Parameter(
#                 'end_date', openapi.IN_QUERY,
#                 description="End date for filtering (YYYY-MM-DD)",
#                 type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE
#             ),
#             # openapi.Parameter(
#             #     'search',
#             #     openapi.IN_QUERY,
#             #     description="Search by expense colums: id, driver first name and last name, description.",
#             #     type=openapi.TYPE_STRING
#             # ),
#         ],
#         responses={200: ContractSerializer(many=True)}
#     )
#     def get(self, request, *args, **kwargs):
#         return super().get(request, *args, **kwargs)
#
#     def perform_create(self, serializer):
#         serializer.save(creator=self.request.user)
#
#
# class ContractRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
#     queryset = Contract.objects.all()
#     serializer_class = ContractSerializer
#
#
# # Generic Views for Transit
# class TransitListCreateView(ListCreateAPIView):
#     queryset = Transit.objects.all()
#
#     def get_serializer_class(self):
#         if self.request.method == 'GET':
#             return TransitGetSerializer
#         return TransitPostSerializer
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
#
#     @swagger_auto_schema(
#         manual_parameters=[
#             openapi.Parameter(
#                 'start_date', openapi.IN_QUERY,
#                 description="Start date for filtering (YYYY-MM-DD)",
#                 type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE
#             ),
#             openapi.Parameter(
#                 'end_date', openapi.IN_QUERY,
#                 description="End date for filtering (YYYY-MM-DD)",
#                 type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE
#             ),
#             # openapi.Parameter(
#             #     'search',
#             #     openapi.IN_QUERY,
#             #     description="Search by expense colums: id, driver first name and last name, description.",
#             #     type=openapi.TYPE_STRING
#             # ),
#         ],
#         responses={200: TransitGetSerializer(many=True)}
#     )
#     def get(self, request, *args, **kwargs):
#         return super().get(request, *args, **kwargs)
#
#     def perform_create(self, serializer):
#         serializer.save(creator=self.request.user)
#
#
# class TransitRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
#     queryset = Transit.objects.all()
#
#     def get_serializer_class(self):
#         if self.request.method == 'GET':
#             return TransitDetailSerializer
#         return TransitPostSerializer
#
#
# # Generic Views for TransitExpense
# class TransitExpenseListCreateView(ListCreateAPIView):
#     queryset = TransitExpense.objects.all()
#     serializer_class = TransitExpenseSerializer
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
#
#     @swagger_auto_schema(
#         manual_parameters=[
#             openapi.Parameter(
#                 'start_date', openapi.IN_QUERY,
#                 description="Start date for filtering (YYYY-MM-DD)",
#                 type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE
#             ),
#             openapi.Parameter(
#                 'end_date', openapi.IN_QUERY,
#                 description="End date for filtering (YYYY-MM-DD)",
#                 type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE
#             ),
#         ],
#         responses={200: TransitExpenseSerializer(many=True)}
#     )
#     def get(self, request, *args, **kwargs):
#         return super().get(request, *args, **kwargs)
#
#     def perform_create(self, serializer):
#         serializer.save(creator=self.request.user)
#
#
# class TransitExpenseRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
#     queryset = TransitExpense.objects.all()
#     serializer_class = TransitExpenseSerializer
#
#
# # Generic Views for TransitIncome
# class TransitIncomeListCreateView(ListCreateAPIView):
#     queryset = TransitIncome.objects.all()
#     serializer_class = TransitIncomeSerializer
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
#
#     @swagger_auto_schema(
#         manual_parameters=[
#             openapi.Parameter(
#                 'start_date', openapi.IN_QUERY,
#                 description="Start date for filtering (YYYY-MM-DD)",
#                 type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE
#             ),
#             openapi.Parameter(
#                 'end_date', openapi.IN_QUERY,
#                 description="End date for filtering (YYYY-MM-DD)",
#                 type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE
#             ),
#         ],
#         responses={200: TransitIncomeSerializer(many=True)}
#     )
#     def get(self, request, *args, **kwargs):
#         return super().get(request, *args, **kwargs)
#
#     def perform_create(self, serializer):
#         serializer.save(creator=self.request.user)
#
#
# class TransitIncomeRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
#     queryset = TransitIncome.objects.all()
#     serializer_class = TransitIncomeSerializer

