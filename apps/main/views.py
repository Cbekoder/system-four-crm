from django.shortcuts import redirect
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from django.utils.dateparse import parse_date
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.utils import timezone
from datetime import timedelta
from rest_framework.response import Response
from apps.users.permissions import IsCEO
from .models import Acquaintance, MoneyCirculation, Expense, Income, DailyRemainder
from .serializers import AcquaintanceSerializer, AcquaintanceDetailSerializer, MoneyCirculationSerializer, \
    ExpenseSerializer, IncomeSerializer, MixedDataSerializer, DailyRemainderSerializer
from .utils import get_remainder_data


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
    queryset = MoneyCirculation.objects.all()
    serializer_class = MoneyCirculationSerializer
    permission_classes = [IsCEO]


    def get_queryset(self):
        self.queryset = self.queryset.filter(type='give')

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
        ],
        responses={200: MoneyCirculationSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(type='give')


class GetMoneyListCreateView(ListCreateAPIView):
    queryset = MoneyCirculation.objects.all()
    serializer_class = MoneyCirculationSerializer
    permission_classes = [IsCEO]

    def get_queryset(self):
        self.queryset = self.queryset.filter(type='get')

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
        ],
        responses={200: MoneyCirculationSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(type='get')


class MoneyCirculationsRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = MoneyCirculation.objects.all()
    serializer_class = MoneyCirculationSerializer
    permission_classes = [IsCEO]


class GeneralExpenseListCreateView(ListCreateAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [IsCEO]

    def get_queryset(self):
        self.queryset = self.queryset.filter(section="general")

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
        ],
        responses={200: ExpenseSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(section="general", user=self.request.user)


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
        serializer.save(section="general", user=self.request.user)


class GeneralIncomeRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = IncomeSerializer
    permission_classes = [IsCEO]

    def get_queryset(self):
        queryset = Income.objects.filter(section="general")
        return queryset


class DailyRemainderView(ListAPIView):
    serializer_class = DailyRemainderSerializer

    def get_queryset(self):
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        start_date = timezone.datetime.strptime(start_date, "%Y-%m-%d").date() if start_date else (
                    timezone.now() - timedelta(days=30)).date()
        end_date = timezone.datetime.strptime(end_date, "%Y-%m-%d").date() if end_date else timezone.now().date()

        queryset = DailyRemainder.objects.filter(created_at__range=[start_date, end_date])
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


###################################################
class MixedHistoryView(APIView):
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
        responses={200: MoneyCirculationSerializer(many=True)}
    )
    def get(self, request):

        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')


        data = get_remainder_data(start_date, end_date)
        response_data = {
            "income": MixedDataSerializer(data["sorted_income"], many=True).data,
            "outcome": MixedDataSerializer(data["sorted_outcome"], many=True).data
        }

        return Response(response_data)
