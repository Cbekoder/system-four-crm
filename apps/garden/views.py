from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import *
from apps.users.permissions import IsCEOOrAdmin, IsAdmin, IsCEO
from apps.main.serializers import ExpenseSerializer, IncomeSerializer
from apps.main.models import Income, Expense
from .serializers import *
from ..users.models import User
from ..users.serializers import UserDetailSerializer, UserPostSerializer
from django.utils.dateparse import parse_date
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class GardenerListCreateView(ListCreateAPIView):
    queryset = Gardener.objects.all()
    serializer_class = GardenerSerializer
    permission_classes = [IsCEOOrAdmin]

class GardenerRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Gardener.objects.all()
    permission_classes = [IsCEO]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return GardenerDetailSerializer
        return GardenerSerializer


class GardenIncomeListCreateView(ListCreateAPIView):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer
    permission_classes = [IsCEOOrAdmin]


    def get_queryset(self):
        queryset = Income.objects.filter(section="garden")
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
        ],
        responses={200: IncomeSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(section="garden", user=self.request.user)


class GardenIncomeRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer
    permission_classes = [IsCEOOrAdmin]

    def get_queryset(self):
        queryset = Income.objects.filter(section="garden")
        return queryset


class GardenExpenseListCreateView(ListCreateAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [IsCEOOrAdmin]

    def get_queryset(self):
        queryset = Expense.objects.filter(section="garden")
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
        ],
        responses={200: ExpenseSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(section="garden", user=self.request.user)

class GardenExpenseRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [IsCEOOrAdmin]

    def get_queryset(self):
        queryset = Expense.objects.filter(section="garden")
        return queryset



class SalaryPaymentListCreateView(ListCreateAPIView):
    queryset = SalaryPayment.objects.all()
    permission_classes = [IsCEOOrAdmin]
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



    # def perform_create(self, serializer):
    #     gardener_id = self.request.data.get('gardener')
    #     if gardener_id:
    #         try:
    #             gardener = Gardener.objects.get(id=gardener_id)
    #             serializer.save(gardener=gardener)
    #             gardener.balance += serializer.validated_data['amount']
    #             gardener.save()
    #         except Gardener.DoesNotExist:
    #             raise ValidationError({"detail": "Gardener not found."})
    #     else:
    #         raise ValidationError({"detail": "Gardener ID is required."})

class SalaryPaymentRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = SalaryPayment.objects.all()
    serializer_class = GardenerSalaryPaymentSerializer
    permission_classes = [IsCEOOrAdmin]





# Admin user views
class GardenUserListCreateAPIView(ListCreateAPIView):
    permission_classes = [IsCEO]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserDetailSerializer
        return UserPostSerializer

    def get_queryset(self):
        queryset = User.objects.filter(section="garden")
        return queryset

    def perform_create(self, serializer):
        serializer.save(section="garden")


class GardenUserRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserDetailSerializer

    def get_queryset(self):
        queryset = User.objects.filter(section="garden")
        return queryset

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserDetailSerializer
        return UserPostSerializer