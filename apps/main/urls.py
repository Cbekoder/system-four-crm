from django.urls import path
from .views import (
    AcquaintanceListCreateView, AcquaintanceRetrieveUpdateDestroyView, GiveMoneyListCreateView,
    GetMoneyListCreateView, MoneyCirculationsRetrieveUpdateDestroyView, GeneralExpenseRetrieveUpdateDestroyView,
    GeneralExpenseListCreateView, GeneralIncomeListCreateView, GeneralIncomeRetrieveUpdateDestroyView
)

urlpatterns = [
    path('acquaintances/', AcquaintanceListCreateView.as_view(), name='acquaintance-list-create'),
    path('acquaintances/<int:pk>/', AcquaintanceRetrieveUpdateDestroyView.as_view(), name='acquaintance-detail'),

    path('circulation/give/', GiveMoneyListCreateView.as_view(), name='give-money-list-create'),
    path('circulation/get/', GetMoneyListCreateView.as_view(), name='get-money-list-create'),
    path('circulation/<int:pk>/', MoneyCirculationsRetrieveUpdateDestroyView.as_view(), name='circulation-retrieve-update-destroy'),

    path('expenses/', GeneralExpenseListCreateView.as_view(), name='general-expenses-list'),
    path('expenses/<int:pk>/', GeneralExpenseRetrieveUpdateDestroyView.as_view(), name='general-expenses-list'),
    
    path('incomes/', GeneralIncomeListCreateView.as_view(), name='general-incomes-list'),
    path('incomes/<int:pk>/', GeneralIncomeRetrieveUpdateDestroyView.as_view(), name='general-incomes-list'),
]
