from django.urls import path
from .views import (
    DriverListCreateView, DriverRetrieveUpdateDestroyView,
    TenantListCreateView, TenantRetrieveUpdateDestroyView,
    ContractorListCreateView, ContractorRetrieveUpdateDestroyView,
    CarListCreateView, CarRetrieveUpdateDestroyView,
    TrailerListCreateView, TrailerRetrieveUpdateDestroyView,
    CarExpenseListCreateView, CarExpenseRetrieveUpdateDestroyView,
    SalaryPaymentListCreateView, SalaryPaymentRetrieveUpdateDestroyView,
    ContractListCreateView, ContractRetrieveUpdateDestroyView,
    TransitListCreateView, TransitRetrieveUpdateDestroyView,
    TransitExpenseListCreateView, TransitExpenseRetrieveUpdateDestroyView,
    TransitIncomeListCreateView, TransitIncomeRetrieveUpdateDestroyView, LogisticUserRetrieveUpdateDestroyAPIView,
    LogisticUserListCreateAPIView, TIRListCreateView, TIRDetailView, TIRRecordListCreateView, TIRRecordDetailView
)

urlpatterns = [
    # Admin URLs
    path('admins/', LogisticUserListCreateAPIView.as_view(), name='logistic-admin-list-create'),
    path('admins/<int:pk>/', LogisticUserRetrieveUpdateDestroyAPIView.as_view(), name='logistic-admin-detail'),
    
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

    # TIR Record URLs
    path('tir-records/', TIRRecordListCreateView.as_view(), name='tir-record-list'),
    path('tir-records/<int:pk>/', TIRRecordDetailView.as_view(), name='tir-record-detail'),

    # CarExpense URLs
    path('car-expenses/', CarExpenseListCreateView.as_view(), name='car-expense-list-create'),
    path('car-expenses/<int:pk>/', CarExpenseRetrieveUpdateDestroyView.as_view(), name='car-expense-detail'),

    # SalaryPayment URLs
    path('salary-payments/', SalaryPaymentListCreateView.as_view(), name='salary-payment-list-create'),
    path('salary-payments/<int:pk>/', SalaryPaymentRetrieveUpdateDestroyView.as_view(), name='salary-payment-detail'),

    # Contract URLs
    path('contracts/', ContractListCreateView.as_view(), name='contract-list-create'),
    path('contracts/<int:pk>/', ContractRetrieveUpdateDestroyView.as_view(), name='contract-detail'),

    # Transit URLs
    path('transits/', TransitListCreateView.as_view(), name='transit-list-create'),
    path('transits/<int:pk>/', TransitRetrieveUpdateDestroyView.as_view(), name='transit-detail'),

    # TransitExpenses URLs
    path('transit-expenses/', TransitExpenseListCreateView.as_view(), name='transit-expenses-list-create'),
    path('transit-expenses/<int:pk>/', TransitExpenseRetrieveUpdateDestroyView.as_view(), name='transit-expenses-detail'),

    # TransitIncome URLs
    path('transit-incomes/', TransitIncomeListCreateView.as_view(), name='transit-income-list-create'),
    path('transit-incomes/<int:pk>/', TransitIncomeRetrieveUpdateDestroyView.as_view(), name='transit-income-detail'),
]
