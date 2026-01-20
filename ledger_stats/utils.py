# ledger_stats/utils.py
from Ledger.models import LedgerRow

def compute_stats():
    """
    Reads ALL ledger rows and returns 3 values:
    - cash_account
    - debtors_in_res
    - total_revenue
    """

    totals = LedgerRow.objects.all().aggregate(
        acc=models.Sum("acc") or 0,
        food=models.Sum("food") or 0,
        bar=models.Sum("bar") or 0,
        laundry=models.Sum("laundry") or 0,
        swimming=models.Sum("swimming") or 0,
        room=models.Sum("room_hire") or 0,
        other=models.Sum("other") or 0,
        t_charge=models.Sum("t_charge") or 0,
        cash=models.Sum("cash") or 0,
        bank=models.Sum("bank_tr") or 0,
        t_ledger=models.Sum("t_ledger") or 0,
        usd=models.Sum("usd_swipe") or 0,
        eco=models.Sum("ecocash_zig") or 0,
        zig=models.Sum("zig_swipe") or 0,
    )

    # Total revenue (sum of all T Charge)
    total_revenue = totals["t_charge"] or 0

    # Cash Account = payments in cash (your formula)
    cash_account = (
        (totals["cash"] or 0)
        + (totals["usd"] or 0)
        + (totals["eco"] or 0)
        + (totals["zig"] or 0)
        + (totals["bank"] or 0)
        + (totals["t_ledger"] or 0)
    )

    # Debtors In Residence = Charges not paid
    debtors_in_res = (
        (totals["t_charge"] or 0)
        - (
            (totals["cash"] or 0)
            + (totals["usd"] or 0)
            + (totals["eco"] or 0)
            + (totals["zig"] or 0)
            + (totals["bank"] or 0)
            + (totals["t_ledger"] or 0)
        )
    )

    return cash_account, debtors_in_res, total_revenue
