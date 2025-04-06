from rest_framework.urls import path
from .views import *


urlpatterns = [
    #Urls for Workers
    path('workers/', WorkerListCreateView.as_view()),
    path('workers/<int:pk>/', WorkerRetrieveUpdateDestroyView.as_view()),

    #Urls for Baskets
    path('baskets/', BasketListCreateView.as_view()),
    path('baskets/<int:pk>/', BasketRetrieveUpdateDestroyView.as_view()),

    #Urls for Daily Work
    path('daily-work/', DailyWorkListCreateView.as_view()),
    path('daily-work/<int:pk>/', DailyWorkRetrieveUpdateDestroyView.as_view()),

    #Urls for Raw Material
    path('raw-materials/', RawMaterialListCreateView.as_view()),
    path('raw-materials/<int:pk>/', RawMaterialRetrieveUpdateDestroyView.as_view()),

    # path('raw-material-usage/', RawMaterialUsageListCreateView.as_view()),
    # path('raw-materials-usage/<int:pk>/', RawMaterialUsageRetrieveUpdateDestroyView.as_view()),

    path('raw-material-history/', RawMaterialHistoryListCreateView.as_view()),
    path('raw-materials-history/<int:pk>/', RawMaterialHistoryRetrieveUpdateDestroyView.as_view()),

    path('suppliers/', SupplierListCreateView.as_view()),
    path('suppliers/<int:pk>/', SupplierRetrieveUpdateDestroyView.as_view()),

    #Urls for Clients
    path('clients/', ClientListCreateView.as_view()),
    path('clients/<int:pk>/', ClientRetrieveUpdateDestroyView.as_view()),

    # Urls for Clients Paying debts
    path('payed-debts/', PayDebtListCreateView.as_view(), name='payed-debts-list'),
    path('payed-debts/<int:pk>/', PayedDebtRetrieveUpdateDestroyView.as_view(), name='payed-debts-about'),

    #Urls for Sales
    path('sales/', SaleListCreateView.as_view(), name='sale-list-create'),
    path('sales/<int:pk>/', SaleRetrieveUpdateDestroyView.as_view(), name='sale-detail'),
    # path('sale-items/', SaleItemListCreateView.as_view(), name='saleitem-list-create'),
    # path('sale-items/<int:pk>/', SaleItemRetrieveUpdateDestroyView.as_view(), name='saleitem-detail'),


    #Urls for Expenses
    path('expenses/', FactoryExpenseListCreateView.as_view()),
    path('expenses/<int:pk>/',FactoryExpenseRetrieveUpdateDestroyView.as_view()),

    #Urls for Income
    path('incomes/',FactoryIncomeListCreateView.as_view()),
    path('incomes/<int:pk>/',FactoryIncomeRetrieveUpdateDestroyView.as_view()),

    #Urls for Salary Payment
    path('salary-payments/', SalaryPaymentListCreateView.as_view()),
    path('salary-payments/<int:pk>/', SalaryPaymentRetrieveUpdateDestroyView.as_view()),

    #Urls for Summary
    path('summary/', FactorySummaryAPIView.as_view()),

]