from rest_framework import serializers
from circulation.models import Loan, Reservation

class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = "__all__"
        read_only_fields = ("borrowed_at", "returned_at")

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = "__all__"
        read_only_fields = ("created_at", "fulfilled")
