from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import DailyLedgerStats
from .serializers import DailyLedgerStatsSerializer

class DailyLedgerStatsViewSet(viewsets.ModelViewSet):
    queryset = DailyLedgerStats.objects.all().order_by("-date")
    serializer_class = DailyLedgerStatsSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        """
        Filter by 'date' query parameter.
        """
        date = self.request.query_params.get("date")
        if date:
            return DailyLedgerStats.objects.filter(date=date)
        return super().get_queryset()

    def create(self, request, *args, **kwargs):
        """
        Create or update ledger stats for the given date.
        """
        date = request.data.get("date")
        if not date:
            return Response({"error": "Date is required"}, status=status.HTTP_400_BAD_REQUEST)

        # If stats exist, update; else create
        instance, created = DailyLedgerStats.objects.get_or_create(date=date)
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
