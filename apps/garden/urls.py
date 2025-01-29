from rest_framework.urls import path
from .views import *

urlpatterns = [
    path('incomes/', IncomeListCreateView.as_view()),
    path('income/<int:pk>', IncomeRetrieveUpdateDestroyView.as_view()),
    path('expenses/', ExpenseListCreateView.as_view()),
    path('expense/<int:pk>', ExpenseRetrieveUpdateDestroyView.as_view()),
    path('gardeners/', GardenerListCreateView.as_view()),
    path('gardener/<int:pk>', GardenerRetrieveUpdateDestroyView.as_view()),
    path('salary_payments/', SalaryPaymentListCreateView.as_view()),

]