
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
  
    customer = serializers.PrimaryKeyRelatedField(queryset=customer.objects.all())
    doctor = serializers.PrimaryKeyRelatedField(queryset=doctor.objects.all())

    class Meta:
        model = Appointment
        fields = ["id", "doctor", "date", "slot", "customer", "created_at", "updated_at"]
        read_only_fields = ["created_at", "updated_at"]
    
    