from django.contrib import admin
from .models import DailyLedgerStats


@admin.register(DailyLedgerStats)
class DailyLedgerStatsAdmin(admin.ModelAdmin):
    list_display = (
        "date",
        "cash_balbf", "cash_acc", "cash_food", "cash_bar",
        "cash_laundry", "cash_swimming", "cash_roomhire",
        "cash_other", "cash_tcharge", "cash_usd", "cash_eco",
        "cash_zig", "cash_cash", "cash_tledger", "cash_banktr",
        "cash_balcf",
        "total_balbf", "total_acc", "total_food", "total_bar",
        "total_laundry", "total_swimming", "total_roomhire",
        "total_other", "total_tcharge", "total_usd", "total_eco",
        "total_zig", "total_cash", "total_tledger", "total_banktr",
        "total_balcf",
        "debtors_in_res",
        "updated_at",
    )

    search_fields = ("date",)
    list_filter = ("date",)
    ordering = ("-date",)

    fieldsets = (
        ("DATE", {
            "fields": ("date",)
        }),

        ("CASH ACCOUNT (Row 1)", {
            "classes": ("collapse",),
            "fields": (
                "cash_balbf", "cash_acc", "cash_food", "cash_bar",
                "cash_laundry", "cash_swimming", "cash_roomhire",
                "cash_other", "cash_tcharge", "cash_usd", "cash_eco",
                "cash_zig", "cash_cash", "cash_tledger", "cash_banktr",
                "cash_balcf",
            )
        }),

        ("TOTALS (Row 2)", {
            "classes": ("collapse",),
            "fields": (
                "total_balbf", "total_acc", "total_food", "total_bar",
                "total_laundry", "total_swimming", "total_roomhire",
                "total_other", "total_tcharge", "total_usd", "total_eco",
                "total_zig", "total_cash", "total_tledger", "total_banktr",
                "total_balcf",
            )
        }),

        ("DEBTORS IN RES (Row 3)", {
            "fields": ("debtors_in_res",)
        }),

        ("SYSTEM FIELDS", {
            "classes": ("collapse",),
            "fields": ("updated_at",),
        }),
    )

    readonly_fields = ("updated_at",)
