from rest_framework import status
from rest_framework.generics import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import *
from drf_spectacular.utils import extend_schema
from .serializers import *
from drf_yasg.utils import swagger_auto_schema

@extend_schema(
    tags=["Gardener"],
    description="Gardener haqida ma'lumotni ko'rsatish"
)
class GardenerListCreateView(ListCreateAPIView):
    queryset = Gardener.objects.all()
    serializer_class = GardenerSerializer
    permission_classes = [IsAuthenticated]

@extend_schema(tags=["Gardener"])
class GardenerRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Gardener.objects.all()
    serializer_class = GardenerSerializer

class IncomeListCreateView(ListCreateAPIView):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer
    permission_classes = [IsAuthenticated]

class IncomeRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer
    permission_classes = [IsAuthenticated]

@extend_schema(
    tags=["Garden Expenses"],
    description="Bog' uchun xarajatlar ro'yxatini ko'rsatish"
)
class ExpenseListCreateView(ListCreateAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]




class ExpenseRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

class SalaryPaymentListCreateView(ListCreateAPIView):
    queryset = SalaryPayment.objects.all()
    serializer_class = SalaryPaymentSerializer
    permission_classes = [IsAuthenticated]

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