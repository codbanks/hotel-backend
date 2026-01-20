from django.contrib import admin
from django.db.models import Max
from django.utils.html import format_html
from django import forms
from .models import HouseStatusReport

# Custom form for admin filter
class CheckoutDateFilterForm(forms.Form):
    checkout_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Checkout Date'
    )

@admin.register(HouseStatusReport)
class HouseStatusReportAdmin(admin.ModelAdmin):
    list_display = (
        'room_no', 'room_type', 'guest_name', 'organization',
        'pax', 'check_in', 'check_out', 'rate', 'out_of_order'
    )

    list_filter = (
        'room_type',
        'out_of_order',
        ('check_in', admin.DateFieldListFilter),
        ('check_out', admin.DateFieldListFilter),
    )

    search_fields = ('room_no', 'guest_name', 'organization')
    ordering = ('room_no', 'check_in')

    # Add a custom filter input box
    change_list_template = "admin/housestatusreport/housestatusreport_change_list.html"


    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Get the date from GET parameters
        checkout_date = request.GET.get('checkout_date')
        if checkout_date:
            qs = qs.filter(check_out=checkout_date)

        # Keep only latest record per room to remove duplicates
        latest_per_room = (
            qs.values('room_no')
            .annotate(latest_id=Max('id'))
            .values_list('latest_id', flat=True)
        )
        return qs.filter(id__in=latest_per_room)
