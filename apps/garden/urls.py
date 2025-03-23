from rest_framework.urls import path
from .views import *

urlpatterns = [
    #Urls for Gardens
    path('gardens/', GardenListCreateView.as_view()),
    path('gardens/<int:pk>/', GardenRetrieveUpdateDestroyView.as_view()),

    #Urls for Expenses
    path('expenses/', GardenExpenseListCreateView.as_view()),
    path('expenses/<int:pk>/', GardenExpenseRetrieveUpdateDestroyView.as_view()),

    #Urls for Incomes
    path('incomes/', GardenIncomeListCreateView.as_view()),
    path('incomes/<int:pk>/', GardenIncomeRetrieveUpdateDestroyView.as_view()),

    #Urls for Gardeners
    path('gardeners/', GardenerListCreateView.as_view()),
    path('gardeners/<int:pk>/', GardenerRetrieveUpdateDestroyView.as_view()),

    #Urls for Salary Payment
    path('salary_payments/', SalaryPaymentListCreateView.as_view()),
    path('salary_payments/<int:pk>', SalaryPaymentRetrieveUpdateDestroyView.as_view()),


]
