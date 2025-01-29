from django.shortcuts import redirect
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.users.permissions import IsCEO
from .models import Acquaintance, MoneyCirculation, Expense, Income
from .serializers import AcquaintanceSerializer, AcquaintanceDetailSerializer, MoneyCirculationSerializer, \
    ExpenseSerializer, IncomeSerializer, MixedDataSerializer
from .utils import get_data


def RedirectToDocs(request):
    return redirect('/docs/')

class AcquaintanceListCreateView(ListCreateAPIView):
    queryset = Acquaintance.objects.all()
    serializer_class = AcquaintanceSerializer
    permission_classes = [IsCEO]

    def perform_create(self, serializer):
        serializer.save(landing=0, debt=0)


class AcquaintanceRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Acquaintance.objects.all()
    permission_classes = [IsCEO]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return AcquaintanceDetailSerializer
        return AcquaintanceSerializer


class GiveMoneyListCreateView(ListCreateAPIView):
    serializer_class = MoneyCirculationSerializer
    permission_classes = [IsCEO]

    def get_queryset(self):
        queryset = MoneyCirculation.objects.filter(type='give')
        return queryset

    def perform_create(self, serializer):
        serializer.save(type='give')


class GetMoneyListCreateView(ListCreateAPIView):
    serializer_class = MoneyCirculationSerializer
    permission_classes = [IsCEO]

    def get_queryset(self):
        queryset = MoneyCirculation.objects.filter(type='get')
        return queryset

    def perform_create(self, serializer):
        serializer.save(type='get')


class MoneyCirculationsRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = MoneyCirculation.objects.all()
    serializer_class = MoneyCirculationSerializer
    permission_classes = [IsCEO]


class GeneralExpenseListCreateView(ListCreateAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [IsCEO]

    def get_queryset(self):
        queryset = Expense.objects.filter(section="general")
        return queryset

    def perform_create(self, serializer):
        serializer.save(sections="general", user=self.request.user)


class GeneralExpenseRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [IsCEO]

    def get_queryset(self):
        queryset = Expense.objects.filter(section="general")
        return queryset


class GeneralIncomeListCreateView(ListCreateAPIView):
    serializer_class = IncomeSerializer
    permission_classes = [IsCEO]

    def get_queryset(self):
        queryset = Income.objects.filter(section="general")
        return queryset

    def perform_create(self, serializer):
        serializer.save(sections="general", user=self.request.user)


class GeneralIncomeRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = IncomeSerializer
    permission_classes = [IsCEO]

    def get_queryset(self):
        queryset = Income.objects.filter(section="general")
        return queryset




###################################################
class MixedHistoryView(APIView):
    def get(self, request):

        data = get_data("asdf", "asdfhasdlfk")
        response_data = {
            "income": MixedDataSerializer(data["sorted_income"], many=True).data,
            "outcome": MixedDataSerializer(data["sorted_outcome"], many=True).data
        }

        return Response(response_data)
