# Ledger/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from datetime import datetime, date
from .models import LedgerRow
from .serializers import LedgerRowSerializer
from rest_framework.permissions import AllowAny


class LedgerRowViewSet(viewsets.ModelViewSet):
    queryset = LedgerRow.objects.all().order_by("-date", "id")
    serializer_class = LedgerRowSerializer
    permission_classes = [AllowAny]

    # ✅ Filtering by date or name
    def get_queryset(self):
        queryset = super().get_queryset()

        # Filter by specific date
        date_str = self.request.query_params.get("date")
        if date_str:
            try:
                d = datetime.strptime(date_str, "%Y-%m-%d").date()
                queryset = queryset.filter(date=d)
            except ValueError:
                pass

        # Optional range filters
        start_date = self.request.query_params.get("start_date")
        end_date = self.request.query_params.get("end_date")
        if start_date and end_date:
            queryset = queryset.filter(date__range=[start_date, end_date])

        # Filter by guest name
        guest_name = self.request.query_params.get("guestname")
        if guest_name:
            queryset = queryset.filter(guest_name__icontains=guest_name)

        return queryset

    # ✅ Create one or multiple ledger rows
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """
        Accepts a single row or list of rows from frontend.
        Automatically computes T Charge and Bal C/F.
        """
        data = request.data
        many = isinstance(data, list)

        serializer = self.get_serializer(data=data, many=many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(
            {"detail": "✅ Ledger entry saved successfully", "data": serializer.data},
            status=status.HTTP_201_CREATED,
        )

    # ✅ Save a single row (used by "Save" button on frontend)
    @action(detail=False, methods=["post"], url_path="row_save")
    def row_save(self, request):
        """
        Frontend sends: { "row": {...} }
        We validate, compute totals, and save.
        """
        row = request.data.get("row", {})
        if not row:
            return Response(
                {"detail": "Row data is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(data=row)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        # Recalculate totals for the given date
        date_str = row.get("date") or date.today().isoformat()
        try:
            d = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            d = date.today()

        totals = LedgerRow.calculate_totals(d)

        return Response(
            {
                "row": LedgerRowSerializer(instance).data,
                "totals": totals,
                "detail": "✅ Row saved successfully",
            },
            status=status.HTTP_200_OK,
        )

    # ✅ Batch save (optional advanced route)
    @action(detail=False, methods=["post"], url_path="block_save")
    def block_save(self, request):
        """
        Accepts a packet of multiple rows and cash/debtors info.
        Used when saving full ledger of a day.
        """
        rows = request.data.get("rows", [])
        cash_account = request.data.get("cashAccount", {})
        debtors_in_res = request.data.get("debtorsInRes", 0)

        if not rows:
            return Response(
                {"detail": "No ledger rows provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        created_rows = []
        with transaction.atomic():
            for row in rows:
                serializer = self.get_serializer(data=row)
                serializer.is_valid(raise_exception=True)
                instance = serializer.save()
                created_rows.append(instance)

        date_str = rows[0].get("date") or date.today().isoformat()
        try:
            d = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            d = date.today()

        totals = LedgerRow.calculate_totals(d)

        return Response(
            {
                "rows": LedgerRowSerializer(created_rows, many=True).data,
                "cashAccount": cash_account,
                "debtorsInRes": debtors_in_res,
                "totals": totals,
                "detail": "✅ Ledger batch saved successfully",
            },
            status=status.HTTP_200_OK,
        )

    # ✅ Get all unique dates
    @action(detail=False, methods=["get"], url_path="dates")
    def ledger_dates(self, request):
        dates = (
            self.queryset.values_list("date", flat=True)
            .distinct()
            .order_by("-date")
        )
        formatted = [d.isoformat() if hasattr(d, "isoformat") else str(d) for d in dates]
        return Response(formatted)

    # ✅ Get calculated totals per date
    @action(detail=False, methods=["get"], url_path="totals")
    def get_totals(self, request):
        """
        Returns computed totals and cash account for a specific date.
        Formula:
          T Charge = Other + Room hire + Swimming + Laundry + Bar + Food + Acc
          Bal C/F  = (T Charge + Bal B/F) - (Bank Tr + T Ledger + Cash + ZIG Swipe + Ecocash Zig + USD Swipe)
        """
        date_str = request.query_params.get("date")
        if not date_str:
            return Response(
                {"detail": "Date query parameter required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            d = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return Response(
                {"detail": "Invalid date format. Use YYYY-MM-DD."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        totals = LedgerRow.calculate_totals(d)
        return Response(
            {"date": date_str, **totals},
            status=status.HTTP_200_OK,
        )

    # ✅ Manual sync from external invoices (optional advanced endpoint)
    @action(detail=False, methods=["post"], url_path="sync_from_invoices")
    def sync_from_invoices(self, request):
        """
        Expected: [{invoice_id, guestName, date, tCharge, bankTr, cash, ...}]
        Updates or creates LedgerRow entries accordingly.
        """
        data = request.data
        if not isinstance(data, list):
            return Response(
                {"error": "Expected a list of invoice packets."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        created, updated = 0, 0
        with transaction.atomic():
            for row in data:
                guest = row.get("guestName")
                invoice_id = row.get("invoice_id")

                instance, created_flag = LedgerRow.objects.update_or_create(
                    folio=invoice_id,
                    defaults={
                        "guest_name": guest,
                        "date": row.get("date", date.today()),
                        "t_charge": row.get("tCharge", 0),
                        "bal_bf": row.get("balBf", 0),
                        "bank_tr": row.get("bankTr", 0),
                        "cash": row.get("cash", 0),
                        "zig_swipe": row.get("zigSwipe", 0),
                        "t_ledger": row.get("tLedger", 0),
                    },
                )
                if created_flag:
                    created += 1
                else:
                    updated += 1

        return Response(
            {"message": "Ledger synced successfully", "created": created, "updated": updated},
            status=status.HTTP_200_OK,
        )
