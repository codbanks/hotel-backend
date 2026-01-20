from django.contrib import admin
from .models import Invoice, InvoiceLine

class InvoiceLineInline(admin.TabularInline):
    model = InvoiceLine
    extra = 1

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("invoice_number", "name", "arrival_date", "departure_date", "created_at")
    search_fields = ("invoice_number", "name", "room_no", "company_account_no")
    inlines = [InvoiceLineInline]

@admin.register(InvoiceLine)
class InvoiceLineAdmin(admin.ModelAdmin):
    list_display = ("invoice", "description", "charges", "credits", "date")
