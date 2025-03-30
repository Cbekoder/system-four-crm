from rest_framework.urls import path
from .views import *


urlpatterns = [
    #Urls for Refrigerators
    path('refrigerators/', RefrigatorListCreateView.as_view()),
    path('refrigerators/<int:pk>/', RefrigatorRetrieveUpdateDestroyView.as_view()),

    #Urls for Expenses
    path('expenses/', FridgeExpenseListCreateView.as_view()),
    path('expenses/<int:pk>/', FridgeExpenseRetrieveUpdateDestroyView.as_view()),

    #Urls for Incomes
    path('incomes/', FridgeIncomeListCreateView.as_view()),
    path('incomes/<int:pk>/', FridgeIncomeRetrieveUpdateDestroyView.as_view()),

    #Urls for Electricity Bills
    path('billings/', ElectricityBillListCreateView.as_view()),
    path('billings/<int:pk>/', ElectricityBillRetrieveUpdateDestroyView.as_view()),

    #Urls for Summary
    path('summary/', FridgeSummaryAPIView.as_view()),

]