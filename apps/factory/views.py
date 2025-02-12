from rest_framework.generics import *
from .serializers import *
from apps.users.permissions import *
from apps.main.models import Expense, Income
from rest_framework.filters import *
from django_filters.rest_framework import DjangoFilterBackend
from apps.main.serializers import ExpenseSerializer, IncomeSerializer
from apps.users.serializers import UserDetailSerializer, UserPostSerializer
from ..users.models import User


class WorkerListCreateView(ListCreateAPIView):
    serializer_class = WorkerSerializer
    queryset = Worker.objects.all()
    permission_classes = [IsCEOOrAdmin]


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

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return DailyWorkSerializer
        return DailyWorkGetSerializer

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

class RawMaterialHistoryRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = RawMaterialHistorySerializer
    queryset = RawMaterialHistory.objects.all()
    permission_classes = [IsCEOOrAdmin]


class FridgeExpenseListCreateView(ListCreateAPIView):
    serializer_class = ExpenseSerializer
    queryset = Expense.objects.all()
    permission_classes = [IsCEOOrAdmin]

    def get_queryset(self):
        queryset = Expense.objects.filter(section="factory")
        return queryset

    def perform_create(self, serializer):
        serializer.save(section="factory", user=self.request.user)

class FridgeIncomeListCreateView(ListCreateAPIView):
    serializer_class = IncomeSerializer
    queryset = Income.objects.all()
    permission_classes = [IsCEOOrAdmin]

    def get_queryset(self):
        queryset = Income.objects.filter(section="factory")
        return queryset

    def perform_create(self, serializer):
        serializer.save(section="factory", user=self.request.user)


class ClientListCreateView(ListCreateAPIView):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()
    permission_classes = [IsCEOOrAdmin]


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





