from rest_framework import serializers
from datetime import date
from .models import LedgerRow

NUMERIC_FIELDS = [
    ("balBf", "bal_bf"),
    ("acc", "acc"),
    ("food", "food"),
    ("bar", "bar"),
    ("laundry", "laundry"),
    ("swimming", "swimming"),
    ("roomHire", "room_hire"),
    ("other", "other"),
    ("tCharge", "t_charge"),
    ("usdSwipe", "usd_swipe"),
    ("ecoCash", "ecocash_zig"),
    ("zigSwipe", "zig_swipe"),
    ("cash", "cash"),
    ("tLedger", "t_ledger"),
    ("bankTr", "bank_tr"),
]

class LedgerRowSerializer(serializers.ModelSerializer):
    balBf = serializers.FloatField(source="bal_bf", default=0, required=False)
    acc = serializers.FloatField(default=0, required=False)
    food = serializers.FloatField(default=0, required=False)
    bar = serializers.FloatField(default=0, required=False)
    laundry = serializers.FloatField(default=0, required=False)
    swimming = serializers.FloatField(default=0, required=False)
    roomHire = serializers.FloatField(source="room_hire", default=0, required=False)
    other = serializers.FloatField(default=0, required=False)
    tCharge = serializers.FloatField(source="t_charge", default=0, required=False)
    usdSwipe = serializers.FloatField(source="usd_swipe", default=0, required=False)
    ecoCash = serializers.FloatField(source="ecocash_zig", default=0, required=False)
    zigSwipe = serializers.FloatField(source="zig_swipe", default=0, required=False)
    cash = serializers.FloatField(default=0, required=False)
    tLedger = serializers.FloatField(source="t_ledger", default=0, required=False)
    bankTr = serializers.FloatField(source="bank_tr", default=0, required=False)
    balCf = serializers.FloatField(source="bal_cf", read_only=True)
    guestName = serializers.CharField(source="guest_name", allow_blank=True, required=False)
    folio = serializers.CharField(allow_blank=True, allow_null=True, required=False)
    pax = serializers.IntegerField(default=1, required=False)
    date = serializers.DateField(required=False)

    class Meta:
        model = LedgerRow
        fields = [
            "id",
            "date",
            "folio",
            "guestName",
            "pax",
            "balBf",
            "acc",
            "food",
            "bar",
            "laundry",
            "swimming",
            "roomHire",
            "other",
            "tCharge",
            "usdSwipe",
            "ecoCash",
            "zigSwipe",
            "cash",
            "tLedger",
            "bankTr",
            "balCf",
        ]

    def validate(self, data):
        if not data.get("date"):
            data["date"] = date.today()

        for cam, mod in NUMERIC_FIELDS:
            raw = data.get(mod, data.get(cam, 0))
            try:
                val = float(raw or 0)
            except (TypeError, ValueError):
                val = 0.0
            data[mod] = round(val, 2)

        data["t_charge"] = round(
            data.get("other", 0)
            + data.get("room_hire", 0)
            + data.get("swimming", 0)
            + data.get("laundry", 0)
            + data.get("bar", 0)
            + data.get("food", 0)
            + data.get("acc", 0),
            2,
        )
        return data

    def create(self, validated_data):
        return LedgerRow.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, val in validated_data.items():
            setattr(instance, attr, val)
        instance.save()
        return instance
