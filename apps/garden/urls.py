from rest_framework.urls import path
from .views import *

urlpatterns = [
    path('expenses/', GardenExpenseListCreateView.as_view()),
    path('expense/<int:pk>', GardenExpenseRetrieveUpdateDestroyView.as_view()),

    path('incomes/', GardenIncomeListCreateView.as_view()),
    path('income/<int:pk>', GardenIncomeRetrieveUpdateDestroyView.as_view()),

    path('gardeners/', GardenerListCreateView.as_view()),
    path('gardener/<int:pk>', GardenerRetrieveUpdateDestroyView.as_view()),

    path('salary_payments/', SalaryPaymentListCreateView.as_view()),

]
