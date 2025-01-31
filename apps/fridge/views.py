from rest_framework.generics import *
from .serializers import *
from apps.users.permissions import *
from rest_framework.permissions import IsAuthenticated


class RefrigatorListCreateView(ListCreateAPIView):
    serializer_class = RefrigeratorSerializer
    queryset = Refrigerator.objects.all()
    permission_classes = [IsCEOOrAdmin]


class RefrigatorRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = RefrigeratorSerializer
    queryset = Refrigerator.objects.all()
    # permission_classes = [IsCEOOrAdmin]

class FridgeExpenseListCreateView(ListCreateAPIView):
    permission_classes = [IsCEOOrAdmin]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return FridgeExpenseSerializer
        return FridgeExpensePostSerializer

    def get_queryset(self):
        queryset = Expense.objects.filter(section='fridge', reason__startswith="expense|")
        return queryset

    def perform_create(self, serializer):
        serializer.save(section="fridge", user=self.request.user)

class FridgeExpenseRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = FridgeExpenseSerializer
    queryset = Expense.objects.all()
    # permission_classes = [IsCEOOrAdmin]

class ElectricityBillListCreateView(ListCreateAPIView):
    permission_classes = [IsCEOOrAdmin]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ElectricityBillSerializer
        return ElectricityBillPostSerializer

    def get_queryset(self):
        queryset = Expense.objects.filter(section='fridge', reason__startswith="electricity|")
        return queryset

    def perform_create(self, serializer):
        serializer.save(section="fridge", user=self.request.user)
