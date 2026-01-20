from django.db import models
from django.utils import timezone

class Invoice(models.Model):
    invoice_number = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255, blank=True)
    
    # Stay Dates - Critical for the Room Sold logic
    arrival_date = models.DateField(default=timezone.now)
    departure_date = models.DateField(null=True, blank=True)
    
    room_no = models.CharField(max_length=20, blank=True)
    room_type = models.CharField(max_length=50, blank=True)
    adults = models.PositiveIntegerField(default=1)
    children = models.PositiveIntegerField(default=0)
    rate_allocated = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    company_account_no = models.CharField(max_length=50, blank=True)
    receptionist = models.CharField(max_length=100, blank=True)
    vat_number = models.CharField(max_length=50, blank=True, default="10005237")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invoice #{self.invoice_number} - {self.name}"

    def get_total(self):
        """Calculates subtotal, VAT, and Grand Total based on Invoice Lines."""
        lines = self.lines.all()
        subtotal = sum(line.charges for line in lines)
        vat = subtotal * 0.15
        total = subtotal + vat
        return {"subtotal": subtotal, "vat": vat, "total": total}

class InvoiceLine(models.Model):
    invoice = models.ForeignKey(Invoice, related_name="lines", on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    description = models.CharField(max_length=255) # e.g., "Accommodation", "Food", "Bar"
    voucher = models.CharField(max_length=100, blank=True)
    charges = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    credits = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.description} ({self.invoice.invoice_number})"