from django.urls import path
from .views import GetMeView, AdminListCreateAPIView, AdminRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('get-me/', GetMeView.as_view(), name='get-me'),
    path('admins/', AdminListCreateAPIView.as_view(), name='admin-list'),
    path('admins/<int:pk>/', AdminRetrieveUpdateDestroyAPIView.as_view(), name='admin-detail'),
]