from django.urls import path
from .views import (
    AcquaintanceListCreateView, AcquaintanceRetrieveUpdateDestroyView, GiveMoneyListCreateView,
    GetMoneyListCreateView, MoneyCirculationsRetrieveUpdateDestroyView, GeneralExpenseRetrieveUpdateDestroyView,
    GeneralExpenseListCreateView, GeneralIncomeListCreateView, GeneralIncomeRetrieveUpdateDestroyView,
    DailyRemainderView, TransactionToAdminListCreateView, TransactionToAdminDetailView,
    TransactionToSectionListCreateView, TransactionToSectionDetailView, CurrencyRateListCreateView,
    TransactionFromSectionListCreateView, TransactionFromSectionDetailView, BankAccountsListCreateView,
    BankAccountsRetrieveUpdateDestroyView, AccountHistoryListCreateView, AccountHistoryRetrieveUpdateDestroyView
)

urlpatterns = [
    path('currency-rates/', CurrencyRateListCreateView.as_view(), name='currency-rate-list'),

    path('acquaintances/', AcquaintanceListCreateView.as_view(), name='acquaintance-list-create'),
    path('acquaintances/<int:pk>/', AcquaintanceRetrieveUpdateDestroyView.as_view(), name='acquaintance-detail'),

    path('circulation/give/', GiveMoneyListCreateView.as_view(), name='give-money-list-create'),
    path('circulation/get/', GetMoneyListCreateView.as_view(), name='get-money-list-create'),
    path('circulation/<int:pk>/', MoneyCirculationsRetrieveUpdateDestroyView.as_view(), name='circulation-retrieve-update-destroy'),
    path('circulation/give/<int:pk>/', MoneyCirculationsRetrieveUpdateDestroyView.as_view(), name='circulation-retrieve-update-destroy'),
    path('circulation/get/<int:pk>/', MoneyCirculationsRetrieveUpdateDestroyView.as_view(), name='circulation-retrieve-update-destroy'),

    path('expenses/', GeneralExpenseListCreateView.as_view(), name='general-expenses-list'),
    path('expenses/<int:pk>/', GeneralExpenseRetrieveUpdateDestroyView.as_view(), name='general-expenses-list'),
    
    path('incomes/', GeneralIncomeListCreateView.as_view(), name='general-incomes-list'),
    path('incomes/<int:pk>/', GeneralIncomeRetrieveUpdateDestroyView.as_view(), name='general-incomes-list'),

    path('transactions-to-admin/', TransactionToAdminListCreateView.as_view(), name='transaction-admin-list'),
    path('transactions-to-admin/<int:pk>/', TransactionToAdminDetailView.as_view(), name='transaction-admin-detail'),

    path('transactions-to-section/', TransactionToSectionListCreateView.as_view(), name='transaction-section-list-create'),
    path('transactions-to-section/<int:pk>/', TransactionToSectionDetailView.as_view(), name='transaction-section-detail'),

    path('transactions-from-section/', TransactionFromSectionListCreateView.as_view(), name='transaction-from-section-list-create'),
    path('transactions-from-section/<int:pk>/', TransactionFromSectionDetailView.as_view(), name='transaction-from-section-detail'),

    path('bank-accounts/', BankAccountsListCreateView.as_view(), name='bank-accounts-list-create'),
    path('bank-accounts/<int:pk>/', BankAccountsRetrieveUpdateDestroyView.as_view(), name='bank-accounts-detail'),

    path('account-history/', AccountHistoryListCreateView.as_view(), name='account-history-list-create'),
    path('account-history/<int:pk>/', AccountHistoryRetrieveUpdateDestroyView.as_view(), name='account-history-detail'),


    path('daily-remainder/', DailyRemainderView.as_view(), name='daily-remainder')
]
