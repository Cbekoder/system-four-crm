from django.urls import path
from .views import GetMeView, AdminListView

urlpatterns = [
    path('get-me/', GetMeView.as_view(), name='get-me'),
    path('admins/', AdminListView.as_view(), name='admin-list'),
]