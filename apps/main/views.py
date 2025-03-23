from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from django.utils.dateparse import parse_date
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.utils import timezone
from datetime import timedelta
from rest_framework.response import Response
from apps.users.permissions import IsCEO, IsAdmin
from .models import Acquaintance, MoneyCirculation, Expense, Income, DailyRemainder, TransactionToAdmin, \
    TransactionToSection, CurrencyRate
from .serializers import AcquaintanceSerializer, AcquaintanceDetailSerializer, MoneyCirculationSerializer, \
    ExpenseSerializer, IncomeSerializer, MixedDataSerializer, DailyRemainderSerializer, \
    TransactionVerifyDetailSerializer, TransactionVerifyActionSerializer, TransactionToAdminSerializer, \
    TransactionToAdminCreateSerializer, TransactionToSectionSerializer, TransactionToSectionCreateSerializer, \
    CurrencyRateSerializer
from .utils import get_remainder_data, calculate_remainder, verification_transaction, verify_transaction, get_summary
from ..common.utils import convert_currency


def RedirectToDocs(request):
    return redirect('/docs/')

class AcquaintanceListCreateView(ListCreateAPIView):
    queryset = Acquaintance.objects.all()
    serializer_class = AcquaintanceSerializer
    permission_classes = [IsCEO]

    def perform_create(self, serializer):
        serializer.save(landing=0, debt=0)


class CurrencyRateListCreateView(ListCreateAPIView):
    permission_classes = [IsAdmin]
    queryset = CurrencyRate.objects.all()
    serializer_class = CurrencyRateSerializer


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
        serializer.save(type='give', creator=self.request.user)


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
        serializer.save(type='get', creator=self.request.user)


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


class TransactionToAdminListCreateView(ListCreateAPIView):
    permission_classes = [IsCEO]

    def get_queryset(self):
        queryset = TransactionToAdmin.objects.all()
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        if start_date:
            queryset = queryset.filter(created_at__date__gte=start_date)
        if end_date:
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
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TransactionToAdminSerializer
        return TransactionToAdminCreateSerializer


class TransactionToAdminDetailView(RetrieveUpdateDestroyAPIView):
    queryset = TransactionToAdmin.objects.all()
    permission_classes = [IsCEO]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TransactionToAdminSerializer
        return TransactionToAdminCreateSerializer


class TransactionToSectionListCreateView(ListCreateAPIView):
    permission_classes = [IsCEO]

    def get_queryset(self):
        queryset = TransactionToSection.objects.all()
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        if start_date:
            queryset = queryset.filter(created_at__date__gte=start_date)
        if end_date:
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
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    # def perform_create(self, serializer):
    #     serializer.save(creator=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TransactionToSectionSerializer
        return TransactionToSectionCreateSerializer


class TransactionToSectionDetailView(RetrieveUpdateDestroyAPIView):
    queryset = TransactionToSection.objects.all()
    permission_classes = [IsCEO]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TransactionToSectionSerializer
        return TransactionToSectionCreateSerializer


class DailyRemainderView(ListAPIView):
    serializer_class = DailyRemainderSerializer

    def get_queryset(self):
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        start_date = timezone.datetime.strptime(start_date, "%Y-%m-%d").date() if start_date else (
                    timezone.now() - timedelta(days=30)).date()
        end_date = timezone.datetime.strptime(end_date, "%Y-%m-%d").date() if end_date else timezone.now().date()

        queryset = DailyRemainder.objects.filter(created_at__range=[start_date, end_date])
        return DailyRemainder.objects.all()

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

        start_date = timezone.datetime.strptime(start_date, "%Y-%m-%d").date() if start_date else (
                timezone.now() - timedelta(days=7)).date()

        if end_date:
            end_date = timezone.datetime.strptime(end_date, "%Y-%m-%d").date()
            remainder = DailyRemainder.objects.filter(created_at=(end_date + timedelta(days=1)))
            remainder_value = remainder.last().amount if remainder.exists() else 0
        else:
            end_date = timezone.now().date()
            remainder_value = request.user.balance

        data = get_summary(start_date, end_date, [request.user])
        response_data = {
            "income": MixedDataSerializer(data["sorted_income"], many=True).data,
            "outcome": MixedDataSerializer(data["sorted_outcome"], many=True).data,
            "remainder": {
                "UZS": remainder_value,
                "RUB": convert_currency("UZS", "RUB", remainder_value),
                "USD": convert_currency("UZS", "USD", remainder_value),
            }
        }

        return Response(response_data)

class TransactionApprovalView(APIView):
    permission_classes = [IsCEO]

    @swagger_auto_schema(
        operation_description="Adminlar tomonidan bajarilgan tranzaksiyalarni ro'yxat sifatida olish uchun GET so'rov.",
        responses={
            200: TransactionVerifyDetailSerializer(many=True),
            400: "Xatolik yuz berdi",
        },
    )
    def get(self, request, *args, **kwargs):

        serializer = TransactionVerifyDetailSerializer(verification_transaction(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=TransactionVerifyActionSerializer,  # POST so'rov tanasi serializerdan olinadi
        responses={
            200: openapi.Response("Muvaffaqiyatli javob", schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "message": openapi.Schema(type=openapi.TYPE_STRING,
                                              description="Tasdiqlash yoki bekor qilish xabari"),
                }
            )),
            400: "Serializer xatoligi",
            404: "Obyekt topilmadi",
            500: "Server xatoligi",
        },
        operation_description="CEO tomonidan tranzaksiyani tasdiqlash yoki bekor qilish uchun POST so'rov."
    )
    def post(self, request, *args, **kwargs):
        serializer = TransactionVerifyActionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        unique_id = serializer.validated_data['unique_id']
        action = serializer.validated_data['action']

        if unique_id == "ALL":
            for transaction in verification_transaction():
                verify_transaction(transaction['unique_id'], action)
            return Response({"message": "All transactions are successfully {}".format(action)})

        return Response({"message": verify_transaction(unique_id, action)})