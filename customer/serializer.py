
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




class AppointmentSerializer(serializers.ModelSerializer):
  

    patient = serializers.StringRelatedField(read_only=True)   # shows username / __str__

    class Meta:
        model  = Appointment
        fields = ["id", "doctor", "date", "slot", "patient", "created_at", "updated_at"]
        read_only_fields = ["patient", "created_at", "updated_at"]

    
    def create(self, validated_data):
        # `patient` comes from the request’s authenticated user (token)
        return super().create({
            **validated_data,
        })