# models.py in HouseStatusReport app
from django.db import models
from Invoice.models import Invoice
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import timedelta

class HouseStatusReport(models.Model):
    room_no = models.CharField(max_length=20)
    room_type = models.CharField(max_length=50, blank=True)
    guest_name = models.CharField(max_length=100, blank=True)
    organization = models.CharField(max_length=100, blank=True)
    pax = models.PositiveIntegerField(default=1)
    check_in = models.DateField(null=True, blank=True)  # represents the day
    check_out = models.DateField(null=True, blank=True)  # full stay end date
    rate = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    out_of_order = models.BooleanField(default=False)
    time = models.CharField(max_length=50, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['room_no', 'check_in']
        verbose_name = "House Status Report"
        verbose_name_plural = "House Status Reports"
        unique_together = ("room_no", "check_in")  # prevents duplicate rows for same room/day

    def __str__(self):
        return f"Room {self.room_no} - {self.guest_name or 'Vacant'} ({self.check_in})"

# -------------------------------
# Signal to create daily occupancy
# -------------------------------
@receiver(post_save, sender=Invoice)
def create_daily_occupancy(sender, instance, **kwargs):
    """
    For each invoice, create a HouseStatusReport row for every day
    between arrival_date (check_in) and departure_date (check_out) inclusive.
    """
    if not instance.room_no or not instance.arrival_date or not instance.departure_date:
        return

    current_date = instance.arrival_date
    while current_date <= instance.departure_date:
        HouseStatusReport.objects.update_or_create(
            room_no=instance.room_no,
            check_in=current_date,
            defaults={
                "room_type": instance.room_type,
                "guest_name": instance.name,
                "organization": instance.company_account_no,
                "pax": instance.adults + instance.children,
                "check_out": instance.departure_date,
                "rate": instance.rate_allocated,
                "time": getattr(instance, "time", ""),
                "out_of_order": False,
            }
        )
        current_date += timedelta(days=1)
