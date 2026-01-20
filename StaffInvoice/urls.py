# StaffInvoice/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
# Make sure to import the views
from .views import StaffInvoiceViewSet, StaffInvoiceLineViewSet 

router = DefaultRouter()

# ❌ OLD: router.register('invoices', StaffInvoiceViewSet)
# ✅ NEW: Explicitly define the basename
router.register('invoices', StaffInvoiceViewSet, basename='staff-invoice') 

# StaffInvoiceLineViewSet already had a basename (stafflines)
router.register('lines', StaffInvoiceLineViewSet, basename='stafflines')

urlpatterns = [
    path('', include(router.urls)),
]