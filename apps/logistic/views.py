from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import (
    Driver, Tenant, Contractor, Car, Trailer, CarExpense, SalaryPayment,
    Contract, Transit, TransitExpense, TransitIncome
)
from .serializers import (
    DriverSerializer, TenantSerializer, ContractorSerializer, CarSerializer, TrailerSerializer,
    CarExpenseSerializer, SalaryPaymentSerializer, ContractSerializer, TransitGetSerializer,
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
    serializer_class = SalaryPaymentSerializer


class SalaryPaymentRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = SalaryPayment.objects.all()
    serializer_class = SalaryPaymentSerializer


# Generic Views for Contract
class ContractListCreateView(ListCreateAPIView):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer


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


class TransitExpenseRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = TransitExpense.objects.all()
    serializer_class = TransitExpenseSerializer


# Generic Views for TransitIncome
class TransitIncomeListCreateView(ListCreateAPIView):
    queryset = TransitIncome.objects.all()
    serializer_class = TransitIncomeSerializer


class TransitIncomeRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = TransitIncome.objects.all()
    serializer_class = TransitIncomeSerializer


# Admin user views
class UserListCreateAPIView(ListCreateAPIView):
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


class UserRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserDetailSerializer

    def get_queryset(self):
        queryset = User.objects.filter(section="logistic")
        return queryset

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserDetailSerializer
        return UserPostSerializer
