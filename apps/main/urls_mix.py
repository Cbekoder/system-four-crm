from django.urls import path

from .views import MixedHistoryView

urlpatterns = [
    path('history/', MixedHistoryView.as_view(), name='history'),
]