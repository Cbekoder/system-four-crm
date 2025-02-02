from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import GetMeView

urlpatterns = [
    path('get-me/', GetMeView.as_view(), name='get-me')
]