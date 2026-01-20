from rest_framework import serializers
from .models import HouseStatusReport

class HouseStatusReportSerializer(serializers.ModelSerializer):
    room_number = serializers.CharField(source='room_no')

    class Meta:
        model = HouseStatusReport
        fields = [
            'id', 'room_number', 'room_type', 'guest_name', 'organization',
            'pax', 'check_in', 'check_out', 'rate', 'out_of_order', 'time',
            'created_at', 'updated_at'
        ]
