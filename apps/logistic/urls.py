from django.urls import path
from .views import (
    DriverListCreateView, DriverRetrieveUpdateDestroyView,
    TenantListCreateView, TenantRetrieveUpdateDestroyView,
    ContractorListCreateView, ContractorRetrieveUpdateDestroyView,
    CarListCreateView, CarRetrieveUpdateDestroyView,
    TrailerListCreateView, TrailerRetrieveUpdateDestroyView,
    CarExpenseListCreateView, CarExpenseRetrieveUpdateDestroyView,
    LogisticSalaryPaymentListCreateView, LogisticSalaryPaymentRetrieveUpdateDestroyView,
    # ContractListCreateView, ContractRetrieveUpdateDestroyView,
    # TransitListCreateView, TransitRetrieveUpdateDestroyView,
    # TransitExpenseListCreateView, TransitExpenseRetrieveUpdateDestroyView,
    # TransitIncomeListCreateView, TransitIncomeRetrieveUpdateDestroyView,
    TIRListCreateView, TIRDetailView, TIRRecordListCreateView, TIRRecordDetailView,
    CompanyListCreateView, CompanyDetailView, WaybillListCreateView, WaybillDetailView, ContractRecordListCreateView,
    ContractRecordDetailView, ContractIncomeListCreateView, ContractIncomeRetrieveUpdateDestroyView,
    WaybillPayoutListCreateView, WaybillPayoutRetrieveUpdateDestroyView, LogisticSummaryAPIView
)

urlpatterns = [
    # Driver URLs
    path('drivers/', DriverListCreateView.as_view(), name='driver-list-create'),
    path('drivers/<int:pk>/', DriverRetrieveUpdateDestroyView.as_view(), name='driver-detail'),

    # Tenant URLs
    path('tenants/', TenantListCreateView.as_view(), name='tenant-list-create'),
    path('tenants/<int:pk>/', TenantRetrieveUpdateDestroyView.as_view(), name='tenant-detail'),

    # Contractor URLs
    path('contractors/', ContractorListCreateView.as_view(), name='contractor-list-create'),
    path('contractors/<int:pk>/', ContractorRetrieveUpdateDestroyView.as_view(), name='contractor-detail'),

    # Car URLs
    path('cars/', CarListCreateView.as_view(), name='car-list-create'),
    path('cars/<int:pk>/', CarRetrieveUpdateDestroyView.as_view(), name='car-detail'),

    # Trailer URLs
    path('trailers/', TrailerListCreateView.as_view(), name='trailer-list-create'),
    path('trailers/<int:pk>/', TrailerRetrieveUpdateDestroyView.as_view(), name='trailer-detail'),

    # TIR URLs
    path('tirs/', TIRListCreateView.as_view(), name='tir-list-create'),
    path('tirs/<int:pk>/', TIRDetailView.as_view(), name='tir-detail'),

    # Company URLs
    path('companies/', CompanyListCreateView.as_view(), name='company-list-create'),
    path('companies/<int:pk>/', CompanyDetailView.as_view(), name='company-detail'),

    # Waybill URLS
    path('transits/', WaybillListCreateView.as_view(), name='waybill-list-create'),
    path('transits/<int:pk>/', WaybillDetailView.as_view(), name='waybill-detail'),

    path('transit-payouts/', WaybillPayoutListCreateView.as_view(), name='waybill-payout-list-create'),
    path('transit-payouts/<int:pk>/', WaybillPayoutRetrieveUpdateDestroyView.as_view(), name='waybill-payout-detail'),

    # TIR Record URLs
    path('tir-records/', TIRRecordListCreateView.as_view(), name='tir-record-list'),
    path('tir-records/<int:pk>/', TIRRecordDetailView.as_view(), name='tir-record-detail'),

    # Contract URLs
    path('contracts/', ContractRecordListCreateView.as_view(), name='contract-list-create'),
    path('contracts/<int:pk>/', ContractRecordDetailView.as_view(), name='contract-detail'),
    path('contract-incomes/', ContractIncomeListCreateView.as_view(), name='contract-income-list-create'),
    path('contract-incomes/<int:pk>/', ContractIncomeRetrieveUpdateDestroyView.as_view(), name='contract-income-detail'),

    # CarExpense URLs
    path('car-expenses/', CarExpenseListCreateView.as_view(), name='car-expense-list-create'),
    path('car-expenses/<int:pk>/', CarExpenseRetrieveUpdateDestroyView.as_view(), name='car-expense-detail'),

    # LogisticSalaryPayment URLs
    path('salary-payments/', LogisticSalaryPaymentListCreateView.as_view(), name='salary-payment-list-create'),
    path('salary-payments/<int:pk>/', LogisticSalaryPaymentRetrieveUpdateDestroyView.as_view(), name='salary-payment-detail'),

    # Summary URLs
    path('summary/', LogisticSummaryAPIView.as_view(), name='logistic-summary'),
]
