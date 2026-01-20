import io
from django.http import FileResponse
from django.db.models import Sum
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

from .models import StaffInvoice, StaffInvoiceLine
from .serializers import StaffInvoiceSerializer, StaffInvoiceLineSerializer

class StaffInvoiceViewSet(viewsets.ModelViewSet):
    """
    Handles Staff Invoice Headers, PDF generation, and Total Annotations.
    """
    serializer_class = StaffInvoiceSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        # Automatically calculate the sum of all lines for each invoice
        return StaffInvoice.objects.annotate(
            calculated_total=Sum('lines__amount')
        ).order_by("-created_at")

    @action(detail=True, methods=["get"])
    def pdf(self, request, pk=None):
        invoice = self.get_object()
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        
        # --- PDF Header ---
        p.setTitle(f"Staff Invoice {invoice.invoice_number}")
        p.setFont("Helvetica-Bold", 16)
        p.drawString(100, 800, "Pumpkin Hotel - STAFF INVOICE")
        
        p.setFont("Helvetica", 10)
        p.drawString(100, 780, f"Invoice No: {invoice.invoice_number}")
        p.drawString(100, 765, f"Date: {invoice.created_at.strftime('%Y-%m-%d')}")
        p.drawString(100, 750, f"Staff Name: {invoice.staff_name}")
        p.drawString(100, 735, f"Staff ID: {invoice.staff_id}")
        p.drawString(100, 720, f"Department: {invoice.department}")

        # --- Table Header ---
        y = 680
        p.setFont("Helvetica-Bold", 10)
        p.drawString(100, y, "Date")
        p.drawString(180, y, "Category")
        p.drawString(280, y, "Description")
        p.drawString(480, y, "Amount ($)")
        p.line(100, y-5, 550, y-5)
        y -= 25

        # --- Fetch and Draw Lines ---
        p.setFont("Helvetica", 10)
        invoice_lines = StaffInvoiceLine.objects.filter(invoice=invoice)
        total_amount = 0
        
        for line in invoice_lines:
            p.drawString(100, y, str(line.date))
            p.drawString(180, y, line.category)
            p.drawString(280, y, line.description)
            p.drawString(480, y, f"{line.amount:.2f}")
            total_amount += line.amount
            y -= 20
            
            # Simple page break logic (if items exceed page)
            if y < 50:
                p.showPage()
                y = 800

        # --- Total ---
        p.line(100, y+10, 550, y+10)
        p.setFont("Helvetica-Bold", 12)
        p.drawString(400, y-20, f"Total Due: ${total_amount:.2f}")

        p.showPage()
        p.save()
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename=f"Staff_Inv_{invoice.invoice_number}.pdf")

class StaffInvoiceLineViewSet(viewsets.ModelViewSet):
    """
    Handles individual lines. Supports filtering by invoice_id and specific dates.
    """
    serializer_class = StaffInvoiceLineSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = StaffInvoiceLine.objects.all().select_related('invoice')
        
        # Filter by Invoice ID if provided in URL (e.g., ?invoice=5)
        invoice_id = self.request.query_params.get("invoice")
        if invoice_id:
            queryset = queryset.filter(invoice_id=invoice_id)
            
        # Filter by Specific Date if provided (e.g., ?date=2023-10-27)
        # Useful for the 'Daily' view in your report
        date = self.request.query_params.get("date")
        if date:
            queryset = queryset.filter(date=date)
            
        return queryset