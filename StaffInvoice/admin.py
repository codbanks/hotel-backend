# StaffInvoice/admin.py

from django.contrib import admin
from .models import StaffInvoice, StaffInvoiceLine

## --- 1. Inline Admin for Invoice Lines ---
# This allows StaffInvoiceLine objects to be edited directly on the StaffInvoice page.
class StaffInvoiceLineInline(admin.TabularInline):
    model = StaffInvoiceLine
    # Defines the fields visible in the inline table
    fields = ('date', 'category', 'description', 'amount') 
    # Optional: sets the default number of empty forms to show
    extra = 1 
    
    # Optional: make sure the category choices are visible
    raw_id_fields = [] 

## --- 2. Main StaffInvoice Admin ---
@admin.register(StaffInvoice)
class StaffInvoiceAdmin(admin.ModelAdmin):
    # Include the inline form for the lines
    inlines = [StaffInvoiceLineInline]

    # Fields displayed in the list view (index page)
    list_display = (
        'invoice_number', 
        'staff_name', 
        'department', 
        'display_total',  # Display the total (calculated below)
        'receptionist', 
        'created_at'
    )
    
    # Fields that can be filtered on the right sidebar
    list_filter = ('department', 'created_at')

    # Fields that can be searched
    search_fields = ('invoice_number', 'staff_name', 'staff_id', 'description')

    # Fields displayed on the edit form, grouped logically
    fieldsets = (
        ('Staff & Invoice Details', {
            'fields': (('invoice_number', 'created_at'), 'staff_name', ('staff_id', 'department'), 'receptionist'),
        }),
        # Total is not editable, it is displayed via the inline table calculation
    )
    
    # Make created_at read-only
    readonly_fields = ('created_at',)

    # --- Calculation for List View ---
    
    # 1. Use database annotation to calculate the total efficiently for the list view
    # This prevents the N+1 problem when loading the admin list.
    def get_queryset(self, request):
        from django.db.models import Sum
        queryset = super().get_queryset(request).annotate(
            _total=Sum('lines__amount')
        )
        return queryset

    # 2. Define the method to display the calculated total
    def display_total(self, obj):
        # Access the annotated field from the queryset
        return f"${obj._total:.2f}" if obj._total is not None else "$0.00"

    # Set a header for the display column
    display_total.short_description = 'Total Amount'


## --- 3. Register StaffInvoiceLine (Optional - only if you want a separate view for lines)
# admin.site.register(StaffInvoiceLine) 
# We usually skip this when using an inline to keep the admin interface clean.