from rest_framework.urls import path
from .views import *


urlpatterns = [
    # Admin URLs
    path('admins/', FactoryUserListCreateAPIView.as_view(), name='factory-admin-list-create'),
    path('admins/<int:pk>/', FactoryUserRetrieveUpdateDestroyAPIView.as_view(), name='factory-admin-detail'),

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

    #Urls for Clients
    path('clients/', ClientListCreateView.as_view()),
    path('clients/<int:pk>/', ClientRetrieveUpdateDestroyView.as_view()),

    #Urls for Sales
    path('sales/', SaleListCreateView.as_view()),
    path('sales/<int:pk>/', SaleRetrieveUpdateDestroyView.as_view()),

    #Urls for Expenses
    path('expenses/', FactoryExpenseListCreateView.as_view()),
    path('expenses/<int:pk>/',FactoryExpenseRetrieveUpdateDestroyView.as_view()),

    #Urls for Income
    path('incomes/',FactoryIncomeListCreateView.as_view()),
    path('incomes/<int:pk>/',FactoryIncomeRetrieveUpdateDestroyView.as_view()),

]