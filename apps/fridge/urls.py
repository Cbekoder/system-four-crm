from rest_framework.urls import path
from .views import *


urlpatterns = [
    # Admin URLs
    path('admins/', FridgeUserListCreateAPIView.as_view(), name='fridge-admin-list-create'),
    path('admins/<int:pk>/', FridgeUserRetrieveUpdateDestroyAPIView.as_view(), name='fridge-admin-detail'),

    #Urls for Refrigerators
    path('refrigerators/', RefrigatorListCreateView.as_view()),
    path('refrigerators/<int:pk>', RefrigatorRetrieveUpdateDestroyView.as_view()),

    #Urls for Expenses
    path('expenses/', FridgeExpenseListCreateView.as_view()),
    path('expenses/<int:pk>', FridgeExpenseRetrieveUpdateDestroyView.as_view()),

    #Urls for Incomes
    path('incomes/', FridgeIncomeListCreateView.as_view()),
    path('incomes/<int:pk>', FridgeIncomeRetrieveUpdateDestroyView.as_view()),

    #Urls for Electricity Bills
    path('billings/', ElectricityBillListCreateView.as_view()),

]