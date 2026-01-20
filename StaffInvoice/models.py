from django.db import models
from django.utils import timezone

class StaffInvoice(models.Model):
    invoice_number = models.CharField(max_length=20, unique=True)
    staff_name = models.CharField(max_length=100)
    staff_id = models.CharField(max_length=50, blank=True)
    department = models.CharField(max_length=100, blank=True)
    receptionist = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # No arrival/departure dates needed for staff credit/requests

    def __str__(self):
        return f"Staff Inv #{self.invoice_number} - {self.staff_name}"

    def get_total(self):
        total = sum(line.amount for line in self.lines.all())
        return total

class StaffInvoiceLine(models.Model):
    CATEGORY_CHOICES = [
        ('Food', 'Food'),
        ('Bar', 'Bar'),
        ('Laundry', 'Laundry'),
        ('Pool', 'Pool'),
        ('Room', 'Room'),
        ('Other', 'Other'),
    ]

    invoice = models.ForeignKey(StaffInvoice, related_name="lines", on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='Food')
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.category} - {self.amount}"