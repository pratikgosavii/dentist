
from rest_framework import serializers
from django.contrib.auth.hashers import make_password

from masters.serializers import slot_serializer
from users.serializer import UserProfileSerializer


from .models import *

class customer_serializer(serializers.ModelSerializer):
    # User fields — readable & writable
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.EmailField(source='user.email', allow_blank=True, required=False)
    dob = serializers.DateField(source='user.dob', required=False, allow_null=True)
    gender = serializers.CharField(source='user.gender', required=False, allow_null=True)
    profile_photo = serializers.ImageField(source='user.profile_photo', required=False, allow_null=True)

    # Read-only fields
    age = serializers.ReadOnlyField(source="user.age")
    patient_id = serializers.ReadOnlyField()

    class Meta:
        model = customer
        fields = [
            'id', 'patient_id', 'is_active', 'profile_photo',
            'first_name', 'last_name', 'email', 'dob', 'gender', 'age'
        ]

    def create(self, validated_data):
        user_data = validated_data.pop('user', {})
        user = self.context['request'].user
        for field, value in user_data.items():
            setattr(user, field, value)
        user.save()
        return customer.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        user = instance.user
        for field, value in user_data.items():
            setattr(user, field, value)
        user.save()
        return super().update(instance, validated_data)




from doctor.models import *


from django.db.models import Sum



class AppointmentSerializer(serializers.ModelSerializer):
    
    slot_details = slot_serializer(source="slot", read_only=True)
    doctor = serializers.PrimaryKeyRelatedField(queryset=doctor.objects.all())
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    customer_details = UserProfileSerializer(source="user", read_only=True)
    
    doctor_details = serializers.SerializerMethodField()

    total_amount = serializers.SerializerMethodField()
    ledger_paid = serializers.SerializerMethodField()
    remaining_amount = serializers.SerializerMethodField()

    class Meta:
        model = Appointment
        fields = [
            "id",
            "doctor",
            "doctor_details",  
            "slot_details",
            "appointment_type",
            "status", 
            "status_display",
            "date",
            "slot",
            "customer_details",
            "concern",
            "created_at",

            # ✅ include new fields in output
            "total_amount",
            "ledger_paid",
            "remaining_amount",
        ]
        read_only_fields = ["created_at", "customer_details"]

    def validate_date(self, value):
        if value < date.today():
            raise serializers.ValidationError("Appointment date cannot be in the past.")
        return value
    
    def get_doctor_details(self, obj):
        # 👇 Lazy import to avoid circular import
        from doctor.serializer import DoctorSerializer  
        return DoctorSerializer(obj.doctor).data if obj.doctor else None

    def get_total_amount(self, obj):
        return AppointmentTreatmentStep.objects.filter(
            appointment_treatment__appointment=obj
        ).aggregate(total=Sum("price"))["total"] or 0

    def get_ledger_paid(self, obj):
        return obj.ledgers.aggregate(total=Sum("amount"))["total"] or 0

    def get_remaining_amount(self, obj):
        total = self.get_total_amount(obj)
        paid = self.get_ledger_paid(obj)
        return total - paid
    


from .models import SupportTicket, TicketMessage

class TicketMessageSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = TicketMessage
        fields = "__all__"
        read_only_fields = ["id", "sender", "created_at"]


class SupportTicketSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    messages = TicketMessageSerializer(many=True, read_only=True)

    class Meta:
        model = SupportTicket
        fields = "__all__"
        read_only_fields = ["id", "is_admin", "user", "status", "created_at", "updated_at"]
