from django.db import models

class DailyLedgerStats(models.Model):
    """
    One record per day.
    Each record has:
    - Cash Account row
    - Totals row
    - Debtors in Residence (single value)
    """
    date = models.DateField(unique=True)

    # CASH ACCOUNT ROW
    cash_balbf = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    cash_acc = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    cash_food = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    cash_bar = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    cash_laundry = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    cash_swimming = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    cash_roomhire = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    cash_other = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    cash_tcharge = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    cash_usd = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    cash_eco = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    cash_zig = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    cash_cash = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    cash_tledger = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    cash_banktr = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    cash_balcf = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    # TOTALS ROW
    total_balbf = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    total_acc = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    total_food = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    total_bar = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    total_laundry = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    total_swimming = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    total_roomhire = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    total_other = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    total_tcharge = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    total_usd = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    total_eco = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    total_zig = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    total_cash = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    total_tledger = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    total_banktr = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    total_balcf = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    # DEBTORS IN RES (single cell)
    debtors_in_res = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Ledger Stats for {self.date}"
