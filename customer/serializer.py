
from rest_framework import serializers
from django.contrib.auth.hashers import make_password


from .models import *

class customer_serializer(serializers.ModelSerializer):

    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)

    class Meta:
        model = customer
        fields = ['id', 'dob', 'gender', 'is_active', 'first_name', 'last_name', 'email']

    def create(self, validated_data):
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')
        email = validated_data.pop('email')

        user = self.context['request'].user
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()

        return customer.objects.create(**validated_data)

    def update(self, instance, validated_data):
        user = self.context['request'].user
        user.first_name = validated_data.pop('first_name', user.first_name)
        user.last_name = validated_data.pop('last_name', user.last_name)
        user.email = validated_data.pop('email', user.email)
        user.save()
        return super().update(instance, validated_data)



from doctor.models import *


class AppointmentSerializer(serializers.ModelSerializer):
    doctor = serializers.PrimaryKeyRelatedField(queryset=doctor.objects.all())
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    class Meta:
        model = Appointment
        fields = [
            "id",
            "doctor",
            "appointment_type",
            "booking_for",
            "status", 
            "status_display",
            "date",
            "time",
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
