from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Import views from your apps
from Invoice.views import InvoiceViewSet, InvoiceLineViewSet
from Ledger.views import LedgerRowViewSet
from HouseStatusReport.views import HouseStatusReportViewSet
from ledger_stats.views import DailyLedgerStatsViewSet

# 1. Setup the DRF Router
router = DefaultRouter()

# Register ViewSets
router.register('invoices', InvoiceViewSet, basename='invoice')
router.register('invoicelines', InvoiceLineViewSet, basename='invoiceline')
router.register('ledger', LedgerRowViewSet, basename='ledger')
router.register('house-status', HouseStatusReportViewSet, basename='house-status')
router.register('ledger-stats', DailyLedgerStatsViewSet, basename='ledger-stats')

# 2. Define URL Patterns
urlpatterns = [
    # --- Router Routes ---
    # This makes endpoints available at /api/v1/invoice/invoices/, etc.
    path('invoice/', include(router.urls)),

    # --- App-specific includes ---
    path('staff-invoice/', include('StaffInvoice.urls')),
    path('house_status_report/', include('HouseStatusReport.urls')),
    path('ledger_stats/', include('ledger_stats.urls')),

    # --- Ledger Custom Routes ---
    # These handle specific logic that doesn't fit standard CRUD
    path('ledger_dates/', LedgerRowViewSet.as_view({'get': 'get_ledger_dates'}), name='ledger-dates'),
    path('ledger/block_save/', LedgerRowViewSet.as_view({'post': 'block_save'}), name='ledger-block-save'),
    path('ledger/totals/', LedgerRowViewSet.as_view({'get': 'get_daily_totals'}), name='ledger-totals'),

    # --- JWT Authentication ---
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # REMOVED: path('', include(router.urls)) 
    # Why? Because having this alongside 'invoice/' creates duplicate paths 
    # and confuses the frontend API calls.
]