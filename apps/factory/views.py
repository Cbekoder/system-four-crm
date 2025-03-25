from datetime import timedelta
from django.db.models import Sum
from django.utils import timezone
from rest_framework import status
from rest_framework.generics import *
from rest_framework.response import Response
from .serializers import *
from apps.users.permissions import IsFactoryAdmin, IsCEO
from apps.main.models import Expense, Income
from rest_framework.filters import *
from django_filters.rest_framework import DjangoFilterBackend
from apps.main.serializers import ExpenseSerializer, IncomeSerializer
from django.utils.dateparse import parse_date
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class WorkerListCreateView(ListCreateAPIView):
    serializer_class = WorkerSerializer
    queryset = Worker.objects.all()
    permission_classes = [IsFactoryAdmin | IsCEO]
    filter_backends = [DjangoFilterBackend,SearchFilter, OrderingFilter]
    search_fields=['first_name','last_name']
    ordering_fields=['balance']


class WorkerRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = WorkerSerializer
    queryset = Worker.objects.all()
    permission_classes = [IsFactoryAdmin | IsCEO]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return WorkerSerializer
        return WorkerGetSerializer

class BasketListCreateView(ListCreateAPIView):
    serializer_class = BasketSerializer
    queryset = Basket.objects.all()
    permission_classes = [IsFactoryAdmin | IsCEO]

    

class BasketRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = BasketSerializer
    queryset = Basket.objects.all()
    permission_classes = [IsFactoryAdmin | IsCEO]


class DailyWorkListCreateView(ListCreateAPIView):
    queryset = UserDailyWork.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    ordering_fields = ['created_at', 'worker']
    search_fields = ['worker__first_name', 'worker__last_name', 'worker__phone_number']
    permission_classes = [IsFactoryAdmin | IsCEO]


    def get_queryset(self):
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
            openapi.Parameter(
                'search',
                openapi.IN_QUERY,
                description="Search by expense colums: id, worker first name,last name and phone number .",
                type=openapi.TYPE_STRING
            ),
        ],
        responses={200: UserDailyWorkDetailSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserDailyWorkDetailSerializer
        return UserDailyWorkCreateSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class DailyWorkRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = UserDailyWork.objects.all()
    permission_classes = [IsFactoryAdmin | IsCEO]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserDailyWorkDetailSerializer
        return UserDailyWorkCreateSerializer

class SupplierListCreateView(ListCreateAPIView):
    serializer_class = SupplierSerializer
    queryset = Supplier.objects.all()
    permission_classes = [IsFactoryAdmin, IsCEO]


class SupplierRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = SupplierSerializer
    queryset = Supplier.objects.all()
    permission_classes = [IsFactoryAdmin, IsCEO]


class RawMaterialListCreateView(ListCreateAPIView):
    serializer_class = RawMaterialSerializer
    queryset = RawMaterial.objects.all()
    permission_classes = [IsFactoryAdmin | IsCEO]

    


class RawMaterialRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = RawMaterialSerializer
    queryset = RawMaterial.objects.all()
    permission_classes = [IsFactoryAdmin | IsCEO]


class RawMaterialHistoryListCreateView(ListCreateAPIView):
    serializer_class = RawMaterialHistorySerializer
    queryset = RawMaterialHistory.objects.all()
    permission_classes = [IsFactoryAdmin | IsCEO]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

class RawMaterialHistoryRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = RawMaterialHistorySerializer
    queryset = RawMaterialHistory.objects.all()
    permission_classes = [IsFactoryAdmin | IsCEO]


    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

# class RawMaterialUsageListCreateView(ListCreateAPIView):
#     serializer_class = RawMaterialUsageSerializer
#     queryset = RawMaterialUsage.objects.all()
#     permission_classes = [IsFactoryAdmin | IsCEO]

    # def perform_create(self, serializer):
    #     serializer.save(creator=self.request.user)

# class RawMaterialUsageRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
#     serializer_class = RawMaterialUsageSerializer
#     queryset = RawMaterialUsage.objects.all()
#     permission_classes = [IsFactoryAdmin | IsCEO]


class FactoryExpenseListCreateView(ListCreateAPIView):
    serializer_class = ExpenseSerializer
    queryset = Expense.objects.all()
    permission_classes = [IsFactoryAdmin | IsCEO]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    ordering_fields = ['created_at', 'amount']
    search_fields=['description','reason']



    def perform_create(self, serializer):
        serializer.save(section="factory", user=self.request.user)


    def get_queryset(self):
        queryset = Expense.objects.filter(section="factory")
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
            openapi.Parameter(
                'search',
                openapi.IN_QUERY,
                description="Search by expense colums: description and reason",
                type=openapi.TYPE_STRING
            ),
        ],
        responses={200: ExpenseSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class FactoryExpenseRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = ExpenseSerializer
    queryset = Expense.objects.all()
    permission_classes = [IsFactoryAdmin | IsCEO]


class FactoryIncomeListCreateView(ListCreateAPIView):
    serializer_class = IncomeSerializer
    queryset = Income.objects.all()
    permission_classes = [IsFactoryAdmin | IsCEO]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    ordering_fields = ['created_at', 'amount']
    search_fields = ['description','reason']

    def get_queryset(self):
        queryset = Income.objects.filter(section="factory")
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
            openapi.Parameter(
                'search',
                openapi.IN_QUERY,
                description="Search by income colums: reason and reason",
                type=openapi.TYPE_STRING
            ),

        ],
        responses={200: IncomeSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(section="factory", user=self.request.user)


class FactoryIncomeRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = IncomeSerializer
    queryset = Income.objects.all()
    permission_classes = [IsFactoryAdmin | IsCEO]


class ClientListCreateView(ListCreateAPIView):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()
    permission_classes = [IsFactoryAdmin | IsCEO]
    filter_backends = [DjangoFilterBackend,  SearchFilter]
    search_fields = ['client__first_name', 'client__last_name', 'client__phone_number']

    def get_queryset(self):
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
            openapi.Parameter(
                'search',
                openapi.IN_QUERY,
                description="Search by expense columns: id, client's first name,last name and phone number .",
                type=openapi.TYPE_STRING
            ),
        ],
        responses={200: ClientSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)




class ClientRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()
    permission_classes = [IsFactoryAdmin | IsCEO]

# class SaleListCreateView(ListCreateAPIView):
#     serializer_class = SaleSerializer
#     queryset = Sale.objects.all()
#     permission_classes = [IsFactoryAdmin | IsCEO]
#     filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
#     ordering_fields = ['created_at', 'client']
#     search_fields = ['client__first_name', 'client__last_name', 'client__phone_number']
#
#     def get_queryset(self):
#         start_date = self.request.query_params.get('start_date')
#         end_date = self.request.query_params.get('end_date')
#
#         if start_date:
#             if not parse_date(start_date):
#                 raise ValidationError({"start_date": "Invalid date format. Use YYYY-MM-DD."})
#             self.queryset = self.queryset.filter(created_at__date__gte=start_date)
#
#         if end_date:
#             if not parse_date(end_date):
#                 raise ValidationError({"end_date": "Invalid date format. Use YYYY-MM-DD."})
#             self.queryset = self.queryset.filter(created_at__date__lte=end_date)
#
#         return self.queryset

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
            openapi.Parameter(
                'search',
                openapi.IN_QUERY,
                description="Search by expense columns: id, client's first name,last name and phone number .",
                type=openapi.TYPE_STRING
            ),
        ],
        responses={200: SaleSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)



# class SaleRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
#     serializer_class = SaleSerializer
#     queryset = Sale.objects.all()
#     permission_classes = [IsFactoryAdmin | IsCEO]



class SalaryPaymentListCreateView(ListCreateAPIView):
    queryset = SalaryPayment.objects.all()
    permission_classes = [IsFactoryAdmin | IsCEO]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    ordering_fields = ['worker', 'worker__balance','amount']
    searching_fields=['worker__first_name','worker__last_name','worker__phone_number']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SalaryPaymentGetSerializer
        return SalaryPaymentPostSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def get_queryset(self):
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
            openapi.Parameter(
                'search',
                openapi.IN_QUERY,
                description="Search by salary payment columns: id, worker's first name,last name and phone number .",
                type=openapi.TYPE_STRING
            ),
        ],
        responses={200: SalaryPaymentGetSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class SalaryPaymentRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = SalaryPaymentGetSerializer
    queryset = SalaryPayment.objects.all()
    permission_classes = [IsFactoryAdmin | IsCEO]

    def get_serializer_class(self):
        if self.request.method == 'PUT' or self.request.method=='PATCH':
            return SalaryPaymentPostSerializer
        return SalaryPaymentGetSerializer


class SaleListCreateView(ListCreateAPIView):
    queryset = Sale.objects.all()
    # serializer_class = SaleSerializer


    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SaleGetSerializer
        return SaleSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# Bitta sotuvni olish, yangilash va o‘chirish (GET, PUT, DELETE)
class SaleRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer

# SaleItem uchun CRUD
class SaleItemListCreateView(ListCreateAPIView):
    queryset = SaleItem.objects.all()
    serializer_class = SaleItemSerializer

class SaleItemRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = SaleItem.objects.all()
    serializer_class = SaleItemSerializer


class FactorySummaryView(ListAPIView):
    permission_classes = [IsFactoryAdmin | IsCEO]

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
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):

        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        section = 'factory'
        if not end_date:
            end_date = timezone.now().date()
        if not start_date:
            start_date = end_date - timedelta(days=30)

        if not section:
            return Response({"error": "section parametri kerak"}, status=400)

        income_total = Income.objects.filter(
            section=section,
            created_at__range=[start_date, end_date]
        ).aggregate(total=Sum('amount'))['total'] or 0

        expense_total = Expense.objects.filter(
            section=section,
            created_at__range=[start_date, end_date]
        ).aggregate(total=Sum('amount'))['total'] or 0

        incomes=Income.objects.filter(section=section, created_at__range=[start_date, end_date])
        expenses=Expense.objects.filter(section=section, created_at__range=[start_date, end_date])
        salary_payments=SalaryPayment.objects.filter( created_at__range=[start_date, end_date])
        sales=Sale.objects.filter( date__range=[start_date, end_date])
        raw_material_histories=RawMaterialHistory.objects.filter( date__range=[start_date, end_date])
        incomes=IncomeSummarySerializer(incomes, many=True).data+SaleSummarySerializer(sales, many=True).data
        expenses=ExpenseSummarySerializer(expenses, many=True).data+SalaryPaymentSummarySerializer(salary_payments, many=True).data+RawMaterialHistorySummarySerializer(raw_material_histories, many=True).data


        return Response({
            'start_date': start_date,
            'end_date': end_date,
            "remainder": self.request.user.balance,
            "section": section,
            "income_total": income_total,
            "expense_total": expense_total,
            "incomes": incomes,
            "expenses": expenses
        })


