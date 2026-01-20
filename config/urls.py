"""
Main URL configuration for the project.

- Admin routes
- JWT authentication routes
- Versioned API routes
- Future API versions can be added under /api/v2/, /api/v3/, etc.

Note:
- Each app (Invoice, API, etc.) manages its own URLs.
- Versioning is done via the URL (api/v1/, api/v2/).
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [

#     /admin/                          -> Django admin
# /api/token/                       -> JWT login
# /api/token/refresh/               -> JWT refresh
# /api/v2/invoices/                 -> List / Create invoices
# /api/v2/invoices/<id>/            -> Retrieve / Update / Delete invoice
# /api/v2/invoicelines/             -> List / Create invoice lines
# /api/v2/invoicelines/<id>/        -> Retrieve / Update / Delete invoice line
# /api/v2/customers/ (future)       -> Customer endpoints
# /api/v2/payments/ (future)        -> Payment endpoints

    # Django admin
    path('admin/', admin.site.urls),

    # JWT Authentication for API clients
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Versioned API routes
    path('api/v1/', include('api.urls')),
    path('api/v2/', include('api.urls')),      # v2 or cross-app API endpoints

    # You can add future versions like:
    # path('api/v3/', include('another_app.urls'))
]
