# Ledger/models.py
from django.db import models
from django.db.models import Sum

class LedgerRow(models.Model):
    date = models.DateField()
    folio = models.CharField(max_length=50, blank=True, null=True)
    guest_name = models.CharField(max_length=255)
    pax = models.IntegerField(default=1)
    bal_bf = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    acc = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    food = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    bar = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    laundry = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    swimming = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    room_hire = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    other = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    t_charge = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    usd_swipe = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    ecocash_zig = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    zig_swipe = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    cash = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    t_ledger = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    bank_tr = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    bal_cf = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        ordering = ['id']

    def save(self, *args, **kwargs):
        """Auto-calculate T Charge and Bal C/F formulas"""
        # ✅ Formula 1: T Charge
        self.t_charge = (
            (self.other or 0)
            + (self.room_hire or 0)
            + (self.swimming or 0)
            + (self.laundry or 0)
            + (self.bar or 0)
            + (self.food or 0)
            + (self.acc or 0)
        )

        # ✅ Formula 2: Bal C/F
        self.bal_cf = (
            (self.bal_bf or 0)
            + (self.t_charge or 0)
            - (
                (self.bank_tr or 0)
                + (self.t_ledger or 0)
                + (self.cash or 0)
                + (self.zig_swipe or 0)
                + (self.ecocash_zig or 0)
                + (self.usd_swipe or 0)
            )
        )
        super().save(*args, **kwargs)

    @classmethod
    def calculate_totals(cls, date_obj):
        """Aggregate totals and compute Cash Account + Debtors in Residence"""
        aggregates = cls.objects.filter(date=date_obj).aggregate(
            bal_bf=Sum('bal_bf') or 0,
            acc=Sum('acc') or 0,
            food=Sum('food') or 0,
            bar=Sum('bar') or 0,
            laundry=Sum('laundry') or 0,
            swimming=Sum('swimming') or 0,
            room_hire=Sum('room_hire') or 0,
            other=Sum('other') or 0,
            t_charge=Sum('t_charge') or 0,
            usd_swipe=Sum('usd_swipe') or 0,
            ecocash_zig=Sum('ecocash_zig') or 0,
            zig_swipe=Sum('zig_swipe') or 0,
            cash=Sum('cash') or 0,
            t_ledger=Sum('t_ledger') or 0,
            bank_tr=Sum('bank_tr') or 0,
            bal_cf=Sum('bal_cf') or 0,
        )

        totals = {k: float(v or 0) for k, v in aggregates.items()}

        # ✅ Cash Account Calculations
        cash_account_tcharge = (
            totals['other'] + totals['room_hire'] + totals['swimming']
            + totals['laundry'] + totals['bar'] + totals['food'] + totals['acc']
        )

        cash_account_balc_f = (
            totals['bal_bf'] + totals['t_charge']
            - (
                totals['bank_tr'] + totals['t_ledger'] + totals['cash']
                + totals['zig_swipe'] + totals['ecocash_zig'] + totals['usd_swipe']
            )
        )

        # ✅ Debtors In Residence
        debtors_in_res = (
            totals['t_charge'] - (
                totals['usd_swipe'] + totals['ecocash_zig']
                + totals['zig_swipe'] + totals['cash']
                + totals['t_ledger'] + totals['bank_tr']
            )
        )

        return {
            "totals": totals,
            "cash_account": {
                **totals,
                "t_charge_box": round(cash_account_tcharge, 2),
                "bal_cf_box": round(cash_account_balc_f, 2),
            },
            "debtors_in_res": round(debtors_in_res, 2)
        }

    def __str__(self):
        return f"{self.guest_name} ({self.date})"
