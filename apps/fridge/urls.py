from rest_framework.urls import path
from .views import *


urlpatterns = [
    path('fridges/', RefrigatorListCreateView.as_view()),
    path('<int:pk>', RefrigatorRetrieveUpdateDestroyView.as_view()),
    path('expenses/', FridgeExpenseListCreateView.as_view()),
    path('expenses/<int:pk>', FridgeExpenseRetrieveUpdateDestroyView.as_view()),
    path('billing/', ElectricityBillListCreateView.as_view()),
]