
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



from rest_framework import serializers
from .models import AppointmentTreatment, AppointmentTreatmentStep

class AppointmentTreatmentStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppointmentTreatmentStep
        fields = ["id", "step_number", "title", "description"]

class AppointmentTreatmentSerializer(serializers.ModelSerializer):
    steps = AppointmentTreatmentStepSerializer(many=True)

    class Meta:
        model = AppointmentTreatment
        fields = ["id", "appointment", "doctor", "treatment", "created_at", "steps"]
        read_only_fields = ["doctor", "appointment"]

    def create(self, validated_data):
        steps_data = validated_data.pop("steps", [])
        appointment_treatment = AppointmentTreatment.objects.create(**validated_data)
        for step in steps_data:
            AppointmentTreatmentStep.objects.create(appointment_treatment=appointment_treatment, **step)
        return appointment_treatment

    def update(self, instance, validated_data):
        steps_data = validated_data.pop("steps", [])
        instance.treatment = validated_data.get("treatment", instance.treatment)
        instance.save()

        # clear old steps & recreate (simple way)
        instance.steps.all().delete()
        for step in steps_data:
            AppointmentTreatmentStep.objects.create(appointment_treatment=instance, **step)
        return instance