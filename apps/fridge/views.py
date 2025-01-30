from rest_framework.generics import *
from .serializers import *
from apps.users.permissions import *
from rest_framework.permissions import IsAuthenticated


class RefrigatorListCreateView(ListCreateAPIView):
    serializer_class = RefrigeratorSerializer
    queryset = Refrigerator.objects.all()
    # permission_classes = [IsCEOOrAdmin]


class RefrigatorRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = RefrigeratorSerializer
    queryset = Refrigerator.objects.all()
    # permission_classes = [IsCEOOrAdmin]

class FridgeExpenseListCreateView(ListCreateAPIView):
    serializer_class = FridgeExpenseSerializer
    queryset = FridgeExpense.objects.all()
    permission_classes = [IsAuthenticated]


class FridgeExpenseRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = FridgeExpenseSerializer
    queryset = FridgeExpense.objects.all()
    # permission_classes = [IsCEOOrAdmin]

class ElectricityBillListCreateView(ListCreateAPIView):
    serializer_class = ElectricityBillSerializer
    queryset = ElectricityBill.objects.all()
    # permission_classes = [IsCEOOrAdmin]
