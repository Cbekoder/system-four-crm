from rest_framework.generics import *
from .serializers import *
from apps.users.permissions import *
from apps.main.models import Expense, Income
from rest_framework.filters import *
from django_filters.rest_framework import DjangoFilterBackend
from apps.main.serializers import ExpenseSerializer, IncomeSerializer
from apps.users.serializers import UserDetailSerializer, UserPostSerializer
from ..users.models import User
from django.utils.dateparse import parse_date
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class WorkerListCreateView(ListCreateAPIView):
    serializer_class = WorkerSerializer
    queryset = Worker.objects.all()
    permission_classes = [IsCEOOrAdmin]
    filter_backends = [DjangoFilterBackend,SearchFilter, OrderingFilter]
    search_fields=['first_name','last_name']
    ordering_fields=['balance']


class WorkerRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = WorkerSerializer
    queryset = Worker.objects.all()
    permission_classes = [IsCEOOrAdmin]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return WorkerSerializer
        return WorkerGetSerializer

class BasketListCreateView(ListCreateAPIView):
    serializer_class = BasketSerializer
    queryset = Basket.objects.all()
    permission_classes = [IsCEOOrAdmin]

class BasketRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = BasketSerializer
    queryset = Basket.objects.all()
    permission_classes = [IsCEOOrAdmin]


class DailyWorkListCreateView(ListCreateAPIView):
    serializer_class = DailyWorkSerializer
    queryset = DailyWork.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    ordering_fields = ['created_at', 'worker']
    search_fields = ['worker__first_name', 'worker__last_name', 'worker__phone_number']
    permission_classes = [IsCEOOrAdmin]

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
                description="Search by expense colums: id, worker first name,last name and phone number .",
                type=openapi.TYPE_STRING
            ),
        ],
        responses={200: DailyWorkGetSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


    def get_serializer_class(self):
        if self.request.method == 'POST':
            return DailyWorkSerializer
        return DailyWorkGetSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

class DailyWorkRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = DailyWorkSerializer
    queryset = DailyWork.objects.all()
    permission_classes = [IsCEOOrAdmin]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return DailyWorkSerializer
        return DailyWorkGetSerializer

class RawMaterialListCreateView(ListCreateAPIView):
    serializer_class = RawMaterialSerializer
    queryset = RawMaterial.objects.all()
    permission_classes = [IsCEOOrAdmin]



class RawMaterialRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = RawMaterialSerializer
    queryset = RawMaterial.objects.all()
    permission_classes = [IsCEOOrAdmin]


class RawMaterialHistoryListCreateView(ListCreateAPIView):
    serializer_class = RawMaterialHistorySerializer
    queryset = RawMaterialHistory.objects.all()
    permission_classes = [IsCEOOrAdmin]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

class RawMaterialHistoryRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = RawMaterialHistorySerializer
    queryset = RawMaterialHistory.objects.all()
    permission_classes = [IsCEOOrAdmin]


class FactoryExpenseListCreateView(ListCreateAPIView):
    serializer_class = ExpenseSerializer
    queryset = Expense.objects.all()
    permission_classes = [IsCEOOrAdmin]
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
    permission_classes = [IsCEOOrAdmin]


class FactoryIncomeListCreateView(ListCreateAPIView):
    serializer_class = IncomeSerializer
    queryset = Income.objects.all()
    permission_classes = [IsCEOOrAdmin]
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
    permission_classes = [IsCEOOrAdmin]


class ClientListCreateView(ListCreateAPIView):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()
    permission_classes = [IsCEOOrAdmin]
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
    permission_classes = [IsCEOOrAdmin]

class SaleListCreateView(ListCreateAPIView):
    serializer_class = SaleSerializer
    queryset = Sale.objects.all()
    permission_classes = [IsCEOOrAdmin]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    ordering_fields = ['created_at', 'client']
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
        responses={200: SaleSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)



class SaleRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = SaleSerializer
    queryset = Sale.objects.all()
    permission_classes = [IsCEOOrAdmin]


# Admin user views
class FactoryUserListCreateAPIView(ListCreateAPIView):
    permission_classes = [IsCEO]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserDetailSerializer
        return UserPostSerializer

    def get_queryset(self):
        queryset = User.objects.filter(section="factory")
        return queryset

    def perform_create(self, serializer):
        serializer.save(section="factory")


class FactoryUserRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserDetailSerializer

    def get_queryset(self):
        queryset = User.objects.filter(section="factory")
        return queryset

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserDetailSerializer
        return UserPostSerializer





