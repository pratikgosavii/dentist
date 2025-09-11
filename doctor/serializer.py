
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
    


class AppointmentMedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appoinment_Medicine
        fields = "__all__"
        read_only_fields = ["user", "doctor"]
    

from customer.serializer import *

class TreatmentSerializer(serializers.ModelSerializer):
    appointment = AppointmentSerializer(read_only=True)
    appointment_id = serializers.PrimaryKeyRelatedField(
        queryset=Appointment.objects.all(), source='appointment', write_only=True
    )

    class Meta:
        model = Treatment
        fields = ['id', 'customer', 'appointment', 'appointment_id', 'title', 'steps']




class TreatmentStepSerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source='doctor.username', read_only=True)
    treatment = TreatmentSerializer(read_only=True)
    treatment_id = serializers.PrimaryKeyRelatedField(
        queryset=Treatment.objects.all(), source='treatment', write_only=True
    )
    class Meta:
        model = TreatmentStep
        fields = ['id', 'treatment', 'treatment_id',  'title', 'description', 'date', 'status', 'doctor_name']
