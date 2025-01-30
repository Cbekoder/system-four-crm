from rest_framework import status
from rest_framework.generics import *
from rest_framework.permissions import IsAuthenticated
from apps.users.permissions import IsCEOOrAdmin, IsAdmin, IsCEO
from .serializers import *


class GardenerListCreateView(ListCreateAPIView):
    queryset = Gardener.objects.all()
    serializer_class = GardenerSerializer
    permission_classes = [IsCEOOrAdmin]


class GardenerRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Gardener.objects.all()
    serializer_class = GardenerSerializer
    permission_classes = [IsCEO]

class IncomeListCreateView(ListCreateAPIView):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer
    permission_classes = [IsCEOOrAdmin]

class IncomeRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer
    permission_classes = [IsCEOOrAdmin]


class ExpenseListCreateView(ListCreateAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [IsCEOOrAdmin]

class ExpenseRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [IsCEOOrAdmin]


class SalaryPaymentListCreateView(ListCreateAPIView):
    queryset = SalaryPayment.objects.all()
    serializer_class = SalaryPaymentSerializer
    permission_classes = [IsCEOOrAdmin]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SalaryPaymentSerializer
        else:
            return SalaryPaymentGetSerializer

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


