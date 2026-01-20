from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HouseStatusReportViewSet

router = DefaultRouter()
router.register('house-status', HouseStatusReportViewSet, basename='house-status')


urlpatterns = [
    path('', include(router.urls)),
]
