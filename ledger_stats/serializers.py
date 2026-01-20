from rest_framework import serializers
from .models import DailyLedgerStats

class DailyLedgerStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyLedgerStats
        fields = "__all__"
