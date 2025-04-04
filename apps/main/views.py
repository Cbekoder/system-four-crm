from django.utils.dateparse import parse_date
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from datetime import timedelta
from apps.users.permissions import IsCEO, IsAdmin
from apps.common.models import CurrencyRate
from apps.common.utils import convert_currency
from .models import Acquaintance, MoneyCirculation, Expense, Income, DailyRemainder, TransactionToAdmin, \
    TransactionToSection, BankAccount, AccountHistory, ACCOUNT_HISTORY_TYPE_CHOICES
from .serializers import AcquaintanceSerializer, AcquaintanceDetailSerializer, MoneyCirculationSerializer, \
    ExpenseSerializer, IncomeSerializer, MixedDataSerializer, DailyRemainderSerializer, \
    TransactionVerifyDetailSerializer, TransactionVerifyActionSerializer, TransactionToAdminSerializer, \
    TransactionToAdminCreateSerializer, TransactionToSectionSerializer, \
    CurrencyRateSerializer, TransactionHistorySerializer, MoneyCirculationPostSerializer, BankAccountsSerializer, \
    AccountHistoryGetSerializer, AccountHistoryPostSerializer
from .utils import get_remainder_data, calculate_remainder, verification_transaction, verify_transaction, get_summary


class CurrencyRateListCreateView(ListCreateAPIView):
    permission_classes = [IsCEO | IsAdmin]
    queryset = CurrencyRate.objects.all()
    serializer_class = CurrencyRateSerializer
    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


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

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return MoneyCirculationSerializer
        return MoneyCirculationPostSerializer

    def perform_create(self, serializer):
        serializer.save(type='give', creator=self.request.user)


class GetMoneyListCreateView(ListCreateAPIView):
    queryset = MoneyCirculation.objects.all()
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

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return MoneyCirculationSerializer
        return MoneyCirculationPostSerializer

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


# Transaction between sections
class TransactionToSectionListCreateView(ListCreateAPIView):
    serializer_class = TransactionToSectionSerializer
    permission_classes = [IsCEO | IsAdmin]
    def get_queryset(self):
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        section = self.request.query_params.get('section')
        is_for = self.request.query_params.get('is_for')
        queryset = TransactionToSection.objects.filter(type='give')
        if start_date:
            queryset = queryset.filter(created_at__date__gte=start_date)
        if end_date:
            queryset = queryset.filter(created_at__date__lte=end_date)
        if is_for is None:
            raise ValidationError({"error": "'is_for' is required"})
        if is_for == "ceo":
            if self.request.user.role == "ceo":
                if section:
                    queryset = queryset.filter(creator=self.request.user, section=section)
                else:
                    queryset = queryset.filter(creator=self.request.user)
            elif self.request.user.role == "admin":
                raise ValidationError({"error": "Only CEO can filter by 'is_for' = 'ceo'"})
            else:
                raise ValidationError({"error": "Нимадир хато кетди."})
        elif is_for == "admin":
            if section is None:
                raise ValidationError({"error": "If 'is_for' is 'admin', 'section' is required"})
            if self.request.user.role == "ceo":
                queryset = queryset.filter(creator__role='admin', creator__section=section, section=section)
            elif self.request.user.role == "admin" and self.request.user.section == section:
                queryset = queryset.filter(creator=self.request.user, section=section)
            else:
                raise ValidationError({"error": "Нимадир хато кетди."})
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
                'section', openapi.IN_QUERY,
                description="Section to filter by. Options: 'logistic', 'fridge', 'garden', 'factory'",
                type=openapi.TYPE_STRING,
                enum=['logistic', 'fridge', 'garden', 'factory', 'general']
            ),
            openapi.Parameter(
                'is_for', openapi.IN_QUERY,
                description="Is For to filter by. Options: 'admin', 'ceo'",
                type=openapi.TYPE_STRING,
                enum=['admin', 'ceo'], required=True
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class TransactionToSectionDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = TransactionToSectionSerializer
    permission_classes = [IsCEO | IsAdmin]
    def get_queryset(self):
        queryset = TransactionToSection.objects.filter(type='give')
        return queryset


class TransactionFromSectionListCreateView(ListCreateAPIView):
    serializer_class = TransactionToSectionSerializer
    permission_classes = [IsCEO | IsAdmin]
    def get_queryset(self):
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        section = self.request.query_params.get('section')
        is_for = self.request.query_params.get('is_for')
        queryset = TransactionToSection.objects.filter(type='get')
        if start_date:
            queryset = queryset.filter(created_at__date__gte=start_date)
        if end_date:
            queryset = queryset.filter(created_at__date__lte=end_date)
        if is_for is None:
            raise ValidationError({"error": "'is_for' is required"})
        if is_for == "ceo":
            if self.request.user.role == "ceo":
                if section:
                    queryset = queryset.filter(creator=self.request.user, section=section)
                else:
                    queryset = queryset.filter(creator=self.request.user)
            elif self.request.user.role == "admin":
                raise ValidationError({"error": "Only CEO can filter by 'is_for' = 'ceo'"})
            else:
                raise ValidationError({"error": "Нимадир хато кетди."})
        elif is_for == "admin":
            if section is None:
                raise ValidationError({"error": "If 'is_for' is 'admin', 'section' is required"})
            if self.request.user.role == "ceo":
                queryset = queryset.filter(creator__role='admin', creator__section=section, section=section)
            elif self.request.user.role == "admin" and self.request.user.section == section:
                queryset = queryset.filter(creator=self.request.user, section=section)
            else:
                raise ValidationError({"error": "Нимадир хато кетди."})
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
                'section', openapi.IN_QUERY,
                description="Section to filter by. Options: 'logistic', 'fridge', 'garden', 'factory'",
                type=openapi.TYPE_STRING,
                enum=['logistic', 'fridge', 'garden', 'factory', 'general'],
            ),
            openapi.Parameter(
                'is_for', openapi.IN_QUERY,
                description="Is For to filter by. Options: 'admin', 'ceo'",
                type=openapi.TYPE_STRING,
                enum=['admin', 'ceo'], required=True
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class TransactionFromSectionDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = TransactionToSectionSerializer
    permission_classes = [IsCEO | IsAdmin]
    def get_queryset(self):
        queryset = TransactionToSection.objects.filter(type='get')
        return queryset
    

class BankAccountsListCreateView(ListCreateAPIView):
    queryset = BankAccount.objects.all()
    permission_classes = [IsCEO]
    serializer_class = BankAccountsSerializer
    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class BankAccountsRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = BankAccount.objects.all()
    permission_classes = [IsCEO]
    serializer_class = BankAccountsSerializer


class AccountHistoryListCreateView(ListCreateAPIView):
    queryset = AccountHistory.objects.all()
    permission_classes = [IsCEO]

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
                'transaction_type', openapi.IN_QUERY,
                description="Filter by transaction type (income or outcome)",
                type=openapi.TYPE_STRING,
                enum=[choice[0] for choice in ACCOUNT_HISTORY_TYPE_CHOICES]
            ),
        ],
        responses={200: AccountHistoryGetSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        transaction_type = self.request.query_params.get('transaction_type')

        queryset = AccountHistory.objects.all()
        if start_date:
            queryset = queryset.filter(created_at__date__gte=start_date)
        if end_date:
            queryset = queryset.filter(created_at__date__lte=end_date)

        if transaction_type is not None and transaction_type in ["income", "outcome"]:
            queryset = queryset.filter(transaction_type=transaction_type)

        return queryset

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return AccountHistoryGetSerializer
        return AccountHistoryPostSerializer


class AccountHistoryRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = AccountHistory.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return AccountHistoryGetSerializer
        return AccountHistoryPostSerializer




class DailyRemainderView(ListAPIView):
    serializer_class = DailyRemainderSerializer

    def get_queryset(self):
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        queryset = DailyRemainder.objects.filter(user=self.request.user)
        if start_date or end_date:
            if start_date:
                queryset = queryset.filter(created_at__date__gte=start_date)
            if end_date:
                queryset = queryset.filter(created_at__date__lte=end_date)
        else:
            queryset = queryset[:30]
      
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
        start_date_str = request.query_params.get('start_date',
                                                  (timezone.now() - timedelta(days=7)).strftime('%Y-%m-%d'))
        end_date_str = request.query_params.get('end_date', timezone.now().strftime('%Y-%m-%d'))

        try:
            start_date = timezone.datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = timezone.datetime.strptime(end_date_str, '%Y-%m-%d')

            start_date = timezone.make_aware(
                timezone.datetime(start_date.year, start_date.month, start_date.day, 0, 0, 0)
            )
            end_date = timezone.make_aware(
                timezone.datetime(end_date.year, end_date.month, end_date.day, 23, 59, 59)
            )
        except ValueError:
            return Response(
                {"error": "Invalid date format. Use YYYY-MM-DD."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if end_date < start_date:
            return Response(
                {"error": "end_date cannot be before start_date."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if end_date.date() == timezone.now().date():
            balance = request.user.balance
        else:
            remainder = DailyRemainder.objects.filter(user=request.user, created_at=(end_date + timedelta(days=1)))
            balance = remainder.last().amount if remainder.exists() else 0



        transactions_data = get_summary(start_date, end_date, [request.user])


        return Response({
            'start_date': start_date_str,
            'end_date': end_date_str,
            'balance': {
                'uzs': convert_currency(request.user.currency_type, "UZS", balance),
                'usd': convert_currency(request.user.currency_type, "USD", balance),
                'rub': convert_currency(request.user.currency_type, "RUB", balance)
            },
            'total_income': {
                'uzs': transactions_data["total_income"],
                'usd': convert_currency("UZS", "USD", transactions_data["total_income"]),
                'rub': convert_currency("UZS", "RUB", transactions_data["total_income"])
            },
            'total_outcome': {
                'uzs': transactions_data["total_outcome"],
                'usd': convert_currency("UZS", "USD", transactions_data["total_outcome"]),
                'rub': convert_currency("UZS", "RUB", transactions_data["total_outcome"])
            },
            'incomes': MixedDataSerializer(transactions_data["incomes_list"], many=True).data,
            'outcomes': MixedDataSerializer(transactions_data["outcomes_list"], many=True).data,
        })


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