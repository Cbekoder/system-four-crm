from rest_framework import status
from rest_framework.generics import *
from apps.users.permissions import IsCEOOrAdmin, IsAdmin, IsCEO
from apps.main.serializers import ExpenseSerializer, IncomeSerializer
from apps.main.models import Income, Expense
from .serializers import *


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
        queryset = Expense.objects.filter(section="garden")
        return queryset

    def perform_create(self, serializer):
        serializer.save(section="garden", user=self.request.user)

class GardenIncomeRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer
    permission_classes = [IsCEOOrAdmin]

    def get_queryset(self):
        queryset = Expense.objects.filter(section="garden")
        return queryset


class GardenExpenseListCreateView(ListCreateAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [IsCEOOrAdmin]

    def get_queryset(self):
        queryset = Expense.objects.filter(section="garden")
        return queryset

    def perform_create(self, serializer):
        serializer.save(section="garden")

class GardenExpenseRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [IsCEOOrAdmin]

    def get_queryset(self):
        queryset = Expense.objects.filter(section="garden")
        return queryset



class SalaryPaymentListCreateView(ListCreateAPIView):
    queryset = SalaryPayment.objects.all()
    permission_classes = [IsCEOOrAdmin]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GardenerSalaryPaymentGetSerializer
        return GardenerSalaryPaymentSerializer

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


