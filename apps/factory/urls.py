from rest_framework.urls import path
from .views import *


urlpatterns = [
    # Admin URLs
    path('admins/', FactoryUserListCreateAPIView.as_view(), name='factory-admin-list-create'),
    path('admins/<int:pk>/', FactoryUserRetrieveUpdateDestroyAPIView.as_view(), name='factory-admin-detail'),

    #Urls for Workers
    path('workers/', WorkerListCreateView.as_view()),
    path('worker/<int:pk>', WorkerRetrieveUpdateDestroyView.as_view()),

    #Urls for Baskets
    path('baskets/', BasketListCreateView.as_view()),
    path('basket/<int:pk>', BasketRetrieveUpdateDestroyView.as_view()),

    #Urls for Daily Work
    path('daily-work/', DailyWorkListCreateView.as_view()),

    #Urls for Raw Material
    path('raw-materials/', RawMaterialListCreateView.as_view()),
    path('raw-material/<int:pk>', RawMaterialRetrieveUpdateDestroyView.as_view()),

    #Urls for Clients
    path('clients/', ClientListCreateView.as_view()),
    path('client/<int:pk>', ClientRetrieveUpdateDestroyView.as_view()),

    #Urls for Sales
    path('sales/', SaleListCreateView.as_view()),
    path('sale/<int:pk>', SaleRetrieveUpdateDestroyView.as_view()),

]