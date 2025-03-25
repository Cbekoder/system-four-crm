from django.urls import path

from .views import MixedHistoryView, TransactionApprovalView

urlpatterns = [
    path('history/', MixedHistoryView.as_view(), name='history'),
    path('verifications/', TransactionApprovalView.as_view(), name='verification'),
]