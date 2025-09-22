
from rest_framework import serializers
from django.contrib.auth.hashers import make_password

from masters.serializers import slot_serializer


from .models import *

class customer_serializer(serializers.ModelSerializer):
    # User fields — readable & writable
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.EmailField(source='user.email', allow_blank=True, required=False)
    dob = serializers.DateField(source='user.dob', required=False, allow_null=True)
    gender = serializers.CharField(source='user.gender', required=False, allow_null=True)

    # Read-only fields
    age = serializers.ReadOnlyField(source="user.age")
    patient_id = serializers.ReadOnlyField()

    class Meta:
        model = customer
        fields = [
            'id', 'patient_id', 'is_active',
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


class AppointmentSerializer(serializers.ModelSerializer):
    slot_details = slot_serializer(source="slot", read_only= True)
    doctor = serializers.PrimaryKeyRelatedField(queryset=doctor.objects.all())
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    class Meta:
        model = Appointment
        fields = [
            "id",
            "doctor",
            "slot_details",
            "appointment_type",
            "booking_for",
            "status", 
            "status_display",
            "date",
            "slot",
            "full_name",
            "phone_number",
            "email",
            "dob",
            "age",
            "gender",
            "concern",
            "created_at",
        ]
        read_only_fields = ["created_at"]

    


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
