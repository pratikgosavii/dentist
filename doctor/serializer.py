
from rest_framework import serializers
from django.contrib.auth.hashers import make_password


from .models import *

class doctor_serializer(serializers.ModelSerializer):

    class Meta:
        model = doctor
        fields = '__all__'
        read_only_fields = ['user']

    image = serializers.ImageField(required=False, allow_null=True)
    



class medicine_serializer(serializers.ModelSerializer):
    class Meta:
        model = medicine
        fields = ['id', 'name', 'brand', 'power', 'form', 'description', 'is_active']
        read_only_fields = ['created_by']
        
    def create(self, validated_data):
        return medicine.objects.create(**validated_data)