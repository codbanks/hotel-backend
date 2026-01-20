from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import HouseStatusReport
from .serializers import HouseStatusReportSerializer
from datetime import datetime
from rest_framework.permissions import AllowAny

class HouseStatusReportViewSet(viewsets.ModelViewSet):
    """
    API endpoint for House Status Reports.
    Supports daily occupancy view and block save for multiple rooms.
    """
    queryset = HouseStatusReport.objects.all()
    serializer_class = HouseStatusReportSerializer
    permission_classes = [AllowAny]

    # -----------------------------
    # GET /house-status/<date>/
    # Fetch all rooms occupied on a specific date
    # -----------------------------
    @action(detail=False, methods=['get'], url_path=r'(?P<date>[\d\-]+)')
    def by_date(self, request, date=None):
        """
        Returns all rooms occupied on the given date.
        Backend now only queries rows where check_in = selected date.
        """
        try:
            target_date = datetime.strptime(date, "%Y-%m-%d").date()
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, 
                            status=status.HTTP_400_BAD_REQUEST)

        # Fetch only the rows for that specific date
        reports = self.queryset.filter(check_in=target_date).order_by('room_no')
        serializer = self.get_serializer(reports, many=True)
        return Response({"rows": serializer.data}, status=status.HTTP_200_OK)

    # -----------------------------
    # POST /house-status/block_save/
    # Save multiple rooms at once
    # -----------------------------
    @action(detail=False, methods=['post'], url_path='block_save')
    def block_save(self, request):
        """
        Saves or updates multiple room rows at once.
        """
        rows = request.data.get("rows", [])
        date = request.data.get("date")

        for row in rows:
            HouseStatusReport.objects.update_or_create(
                room_no=row.get("room_number"),
                check_in=row.get("check_in") or date,
                defaults={
                    "room_type": row.get("room_type", ""),
                    "guest_name": row.get("guest_name", ""),
                    "organization": row.get("organization", ""),
                    "pax": row.get("pax", 1),
                    "check_out": row.get("check_out"),
                    "rate": row.get("rate", 0),
                    "out_of_order": row.get("out_of_order", False),
                    "time": row.get("time", ""),
                }
            )
        return Response({"message": "All rooms saved successfully ✅"}, 
                        status=status.HTTP_200_OK)
