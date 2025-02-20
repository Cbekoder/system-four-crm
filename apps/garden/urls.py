from rest_framework.urls import path
from .views import *

urlpatterns = [
    # Admin URLs
    path('admins/', GardenUserListCreateAPIView.as_view(), name='garden-admin-list-create'),
    path('admins/<int:pk>/', GardenUserRetrieveUpdateDestroyAPIView.as_view(), name='garden-admin-detail'),

    path('expenses/', GardenExpenseListCreateView.as_view()),
    path('expenses/<int:pk>', GardenExpenseRetrieveUpdateDestroyView.as_view()),

    path('incomes/', GardenIncomeListCreateView.as_view()),
    path('incomes/<int:pk>', GardenIncomeRetrieveUpdateDestroyView.as_view()),

    path('gardeners/', GardenerListCreateView.as_view()),
    path('gardeners/<int:pk>', GardenerRetrieveUpdateDestroyView.as_view()),

    path('salary_payments/', SalaryPaymentListCreateView.as_view()),

]
