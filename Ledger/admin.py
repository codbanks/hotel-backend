from django.contrib import admin
from django.db.models import Sum
from .models import LedgerRow

@admin.register(LedgerRow)
class LedgerRowAdmin(admin.ModelAdmin):
    list_display = [
        'date', 'guest_name', 'folio', 'pax', 'bal_bf', 'acc', 'food', 'bar',
        'laundry', 'swimming', 'room_hire', 'other', 't_charge',
        'usd_swipe', 'ecocash_zig', 'zig_swipe', 'cash', 't_ledger',
        'bank_tr', 'bal_cf'
    ]
    list_filter = ['date']
    search_fields = ['guest_name', 'folio']
    list_editable = [
        'bal_bf', 'acc', 'food', 'bar', 'laundry', 'swimming', 'room_hire',
        'other', 't_charge', 'usd_swipe', 'ecocash_zig', 'zig_swipe',
        'cash', 't_ledger', 'bank_tr'
    ]

    change_list_template = "admin/change_list.html"  # keep default template

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context)
        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        # Helper to safely sum values
        def safe(value):
            return value if value is not None else 0

        totals = qs.aggregate(
            bal_bf=Sum('bal_bf'), acc=Sum('acc'), food=Sum('food'), bar=Sum('bar'),
            laundry=Sum('laundry'), swimming=Sum('swimming'), room_hire=Sum('room_hire'),
            other=Sum('other'), t_charge=Sum('t_charge'), usd_swipe=Sum('usd_swipe'),
            ecocash_zig=Sum('ecocash_zig'), zig_swipe=Sum('zig_swipe'), cash=Sum('cash'),
            t_ledger=Sum('t_ledger'), bank_tr=Sum('bank_tr'), bal_cf=Sum('bal_cf')
        )
        totals = {k: safe(v) for k, v in totals.items()}

        # Cash account can be customized; here we just reuse totals as example
        cash_account = {k: safe(v) for k, v in totals.items()}

        # Debtors in Res formula
        debtors_in_res = (
            safe(totals['t_charge']) -
            (safe(totals['usd_swipe']) +
             safe(totals['ecocash_zig']) +
             safe(totals['zig_swipe']) +
             (safe(totals['cash']) - safe(totals['bank_tr'])))
        )

        extra_context = extra_context or {}
        extra_context['ledger_totals'] = totals
        extra_context['ledger_cash_account'] = cash_account
        extra_context['ledger_debtors_in_res'] = debtors_in_res

        response.context_data.update(extra_context)
        return response

    # Optional: display totals in admin footer using custom methods
    def get_totals(self, obj):
        return self._totals
    get_totals.short_description = 'Totals'
