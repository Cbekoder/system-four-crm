from rest_framework.urls import path
from .views import *


urlpatterns = [
    path('refrigerators/', RefrigatorListCreateView.as_view()),
    path('refrigerator/<int:pk>', RefrigatorRetrieveUpdateDestroyView.as_view()),
    path('expenses/', FridgeExpenseListCreateView.as_view()),
    path('expense/<int:pk>', FridgeExpenseRetrieveUpdateDestroyView.as_view()),
    path('billings/', ElectricityBillListCreateView.as_view()),
]