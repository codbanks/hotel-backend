from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DailyLedgerStatsViewSet

router = DefaultRouter()
router.register(r'daily_ledger_stats', DailyLedgerStatsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
