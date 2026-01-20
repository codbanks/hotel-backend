# hotelLedger/signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum
from .models import LedgerRow, DebtorsInRes

def update_daily_totals(date):
    # 1️⃣ Gather all normal rows for this date
    rows = LedgerRow.objects.filter(date=date, is_total_row=False)

    # 2️⃣ Update each row’s Bal C/F
    for row in rows:
        row.update_bal_cf()

    # 3️⃣ Compute totals
    totals = rows.aggregate(
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

    # 4️⃣ Replace the totals row safely
    LedgerRow.objects.filter(date=date, is_total_row=True).delete()
    LedgerRow.objects.create(
        date=date,
        guest_name='TOTALS',
        folio='TOTALS',
        is_total_row=True,
        **totals
    )

    # 5️⃣ Compute Debtors In Res using the totals row logic
    debtors_total = (
        (totals['bal_bf'] or 0)
        + (totals['t_charge'] or 0)
        - (totals['bank_tr'] or 0)
        - (totals['t_ledger'] or 0)
        - (totals['cash'] or 0)
        - (totals['zig_swipe'] or 0)
        - (totals['ecocash_zig'] or 0)
        - (totals['usd_swipe'] or 0)
    )

    DebtorsInRes.objects.update_or_create(
        date=date,
        defaults={'total': debtors_total}
    )

    print(f"✅ Totals updated for {date} | DebtorsInRes = {debtors_total}")
    

@receiver(post_save, sender=LedgerRow)
def ledger_post_save(sender, instance, **kwargs):
    if not instance.is_total_row:
        update_daily_totals(instance.date)


@receiver(post_delete, sender=LedgerRow)
def ledger_post_delete(sender, instance, **kwargs):
    if not instance.is_total_row:
        update_daily_totals(instance.date)
