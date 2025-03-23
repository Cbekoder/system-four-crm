from django.urls import path

from .views import MixedHistoryView, TransactionApprovalView, CurrencyRateListCreateView

urlpatterns = [
    path('currency-rates/', CurrencyRateListCreateView.as_view(), name='currency-rate-list'),
    path('history/', MixedHistoryView.as_view(), name='history'),
    path('verifications/', TransactionApprovalView.as_view(), name='verification'),
]