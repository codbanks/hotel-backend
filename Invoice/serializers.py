from rest_framework import serializers
from .models import Invoice, InvoiceLine

class InvoiceLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceLine
        fields = "__all__"

    def validate_description(self, value):
        if not value or value.strip() == '':
            raise serializers.ValidationError("Description is required")
        return value


class InvoiceSerializer(serializers.ModelSerializer):
    lines = InvoiceLineSerializer(many=True, read_only=True)

    class Meta:
        model = Invoice
        fields = "__all__"
