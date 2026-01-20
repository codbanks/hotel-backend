from rest_framework import serializers
from .models import StaffInvoice, StaffInvoiceLine

class StaffInvoiceLineSerializer(serializers.ModelSerializer):
    # This field pulls the staff name from the parent StaffInvoice model
    # It allows the frontend to group totals by staff member dynamically
    staff_name = serializers.ReadOnlyField(source='invoice.staff_name')

    class Meta:
        model = StaffInvoiceLine
        fields = [
            'id', 
            'invoice', 
            'staff_name', 
            'date', 
            'category', 
            'description', 
            'amount'
        ]

class StaffInvoiceSerializer(serializers.ModelSerializer):
    lines = StaffInvoiceLineSerializer(many=True, read_only=True)
    
    # Uses the annotated 'calculated_total' from the ViewSet for performance
    total = serializers.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        source='calculated_total', 
        read_only=True, 
        required=False
    )

    class Meta:
        model = StaffInvoice
        fields = [
            'id', 
            'invoice_number', 
            'staff_name', 
            'staff_id', 
            'department', 
            'receptionist', 
            'created_at', 
            'lines', 
            'total'
        ]

    def get_total(self, obj):
        # Fallback logic for the total if annotation is missing
        if hasattr(obj, 'calculated_total') and obj.calculated_total is not None:
            return obj.calculated_total
        return sum(line.amount for line in obj.lines.all())