from rest_framework import viewsets
from rest_framework.decorators import action
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from .models import Invoice, InvoiceLine
from .serializers import InvoiceSerializer, InvoiceLineSerializer
import io
from rest_framework.permissions import AllowAny

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all().order_by("-created_at")
    serializer_class = InvoiceSerializer
    permission_classes = [AllowAny]  # <-- public


    @action(detail=True, methods=["get"])
    def pdf(self, request, pk=None):
        invoice = self.get_object()
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        p.setTitle(f"Invoice {invoice.invoice_number}")
        p.drawString(100, 800, f"Pumpkin Hotel (Pvt) Ltd")
        p.drawString(100, 780, f"Invoice No: {invoice.invoice_number}")
        p.drawString(100, 760, f"Name: {invoice.name}")
        p.drawString(100, 740, f"Address: {invoice.address}")
        y = 700
        for line in invoice.lines.all():
            p.drawString(100, y, f"{line.date} - {line.description} - {line.charges}")
            y -= 20
        totals = invoice.get_total()
        p.drawString(100, y - 40, f"Subtotal: {totals['subtotal']}")
        p.drawString(100, y - 60, f"VAT: {totals['vat']}")
        p.drawString(100, y - 80, f"Total: {totals['total']}")
        p.showPage()
        p.save()
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename=f"Invoice_{invoice.invoice_number}.pdf")


class InvoiceLineViewSet(viewsets.ModelViewSet):
    serializer_class = InvoiceLineSerializer
    permission_classes = [AllowAny]  # <-- public

    def get_queryset(self):
        queryset = InvoiceLine.objects.all()
        invoice_id = self.request.query_params.get("invoice")
        if invoice_id:
            queryset = queryset.filter(invoice_id=invoice_id)
        return queryset
