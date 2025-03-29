from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import OrderingFilter
from rest_framework.generics import *
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *
from apps.users.permissions import IsFridgeAdmin, IsCEO
from django.utils.dateparse import parse_date
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from datetime import timedelta
from django.db.models import Sum
from django.utils import timezone


class RefrigatorListCreateView(ListCreateAPIView):
    serializer_class = RefrigeratorSerializer
    queryset = Refrigerator.objects.all()
    permission_classes = [IsFridgeAdmin | IsCEO]


class RefrigatorRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = RefrigeratorSerializer
    queryset = Refrigerator.objects.all()
    permission_classes = [IsFridgeAdmin | IsCEO]

    def delete(self, request, *args, **kwargs):
        if not request.user.role == 'CEO':
            return Response(
                {"detail": "Only CEO can delete this item."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().delete(request, *args, **kwargs)

class FridgeExpenseListCreateView(ListCreateAPIView):
    permission_classes = [IsFridgeAdmin | IsCEO]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['created_at', 'price']

    def get_serializer_class(self):
        if self.request.method == "GET":
            return FridgeExpenseSerializer
        return FridgeExpensePostSerializer

    def get_queryset(self):
        queryset = Expense.objects.filter(section='fridge')
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
        responses={200: FridgeExpenseSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def perform_create(self, serializer):
        user = self.request.user
        amount = serializer.validated_data.get("amount", 0)

        amount=convert_currency(serializer.validated_data.get("currency_type", "UZS"), user.currency_type, amount)
        if user.balance < amount:
            raise ValidationError({"detail": "Yetarli mablag' mavjud emas!"})

        with (transaction.atomic()):
            user.balance -= amount
            user.save(update_fields=["balance"])
            serializer.save(section="fridge", user=user)

class FridgeExpenseRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = FridgeExpenseSerializer
    queryset = Expense.objects.all()
    permission_classes = [IsFridgeAdmin | IsCEO]


class FridgeIncomeListCreateView(ListCreateAPIView):
    permission_classes = [IsFridgeAdmin | IsCEO]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return FridgeIncomeSerializer
        return FridgeIncomePostSerializer

    def get_queryset(self):
        self.queryset = Income.objects.filter(section='fridge')
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
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATE
            ),
            openapi.Parameter(
                'end_date', openapi.IN_QUERY,
                description="End date for filtering (YYYY-MM-DD)",
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATE
            ),
        ],
        responses={200: FridgeIncomeSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(section="fridge", user=self.request.user)

class FridgeIncomeRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Income.objects.all()
    serializer_class = FridgeIncomeSerializer
    permission_classes = [IsFridgeAdmin | IsCEO]


class ElectricityBillListCreateView(ListCreateAPIView):
    permission_classes = [IsFridgeAdmin | IsCEO]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ElectricityBillSerializer
        return ElectricityBillPostSerializer

    def get_queryset(self):
        self.queryset = Expense.objects.filter(section='fridge', reason="electricity|1")
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
        responses={200: ElectricityBillSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def perform_create(self, serializer):
        user = self.request.user
        amount = serializer.validated_data.get("amount", 0)

        amount = convert_currency(serializer.validated_data.get("currency_type", "UZS"), user.currency_type, amount)
        if user.balance < amount:
            raise ValidationError({"detail": "Yetarli mablag' mavjud emas!"})

        with (transaction.atomic()):
            user.balance -= amount
            user.save(update_fields=["balance"])
            serializer.save(section="fridge", user=user)




class FridgeSummaryView(APIView):
    permission_classes = [IsFridgeAdmin | IsCEO]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'start_date', openapi.IN_QUERY,
                description="Boshlang'ich sana (YYYY-MM-DD)",
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATE
            ),
            openapi.Parameter(
                'end_date', openapi.IN_QUERY,
                description="Tugash sanasi (YYYY-MM-DD)",
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATE
            ),

        ]
    )
    def get(self, request):

        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        section = 'fridge'
        if not end_date:
            end_date = timezone.now().date()
        if not start_date:
            start_date = end_date - timedelta(days=30)

        if not section:
            return Response({"error": "section parametri kerak"}, status=400)



        incomes=Income.objects.filter(section=section, created_at__range=[start_date, end_date])

        expenses=Expense.objects.filter(section=section, created_at__range=[start_date, end_date])
        print(f"Filtered Expenses Count: {expenses, len(expenses)}")

        incomes=IncomeSummarySerializer(incomes, many=True).data
        expenses=ExpenseSummarySerializer(expenses, many=True).data

        print(f"Filtered Expenses Count: {expenses,len(expenses)}")
        # print(f"Filtered Expenses: {expenses.values_list('id', 'created_at', 'section')}")
        print(Expense.objects.filter(section=section))

        income_total = (Income.objects.filter(
            section=section,
            created_at__range=[start_date, end_date]
        ).aggregate(total=Sum('amount'))['total']) or 0



        expense_total = (Expense.objects.filter(
            section=section,
            created_at__range=[start_date, end_date]
        ).aggregate(total=Sum('amount'))['total'])


        return Response({
            'start_date': start_date,
            'end_date': end_date,
            'balance': {
                'uzs': convert_currency(request.user.currency_type, "UZS", request.user.balance),
                'usd': convert_currency(request.user.currency_type, "USD", request.user.balance),
                'rub': convert_currency(request.user.currency_type, "RUB", request.user.balance)
            },
            "section": section,
            "income_total": income_total,
            "expense_total": expense_total,
            "incomes": incomes,
            "expenses": expenses
        })

