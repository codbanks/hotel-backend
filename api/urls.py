from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from Invoice.views import InvoiceViewSet, InvoiceLineViewSet
from Ledger.views import LedgerRowViewSet
from HouseStatusReport.views import HouseStatusReportViewSet
from ledger_stats.views import DailyLedgerStatsViewSet

# DRF Router
router = DefaultRouter()

# ----- Invoice routes -----
router.register('invoices', InvoiceViewSet, basename='invoice')
router.register('invoicelines', InvoiceLineViewSet, basename='invoiceline')

# ----- Ledger routes -----
router.register('ledger', LedgerRowViewSet, basename='ledger')

# ----- House Status Report routes -----
router.register('house-status', HouseStatusReportViewSet, basename='house-status')

router.register('ledger-stats', DailyLedgerStatsViewSet, basename='ledger-stats')

urlpatterns = [
    # Invoice routes
    path('invoice/', include(router.urls)),
    # Add this line:
    path('staff-invoice/', include('StaffInvoice.urls')),

    # Ledger extra routes
    path('ledger_dates/', LedgerRowViewSet.as_view({'get': 'get_ledger_dates'}), name='ledger-dates'),
    path('ledger/block_save/', LedgerRowViewSet.as_view({'post': 'block_save'}), name='ledger-block-save'),
    path('ledger/totals/', LedgerRowViewSet.as_view({'get': 'get_daily_totals'}), name='ledger-totals'),

    # JWT auth
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Include HouseStatusReport URLs
    path('house_status_report/', include('HouseStatusReport.urls')),

    # ✅ Include ledger_stats routes (as instructed)
    path('ledger_stats/', include('ledger_stats.urls')),

    # Default router (Invoice + Ledger + HouseStatusReport)
    path('', include(router.urls)),
]
