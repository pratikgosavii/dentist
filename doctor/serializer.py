
from rest_framework import serializers
from django.contrib.auth.hashers import make_password


from .models import *
from customer.serializer import *
from rest_framework import serializers


class doctor_serializer(serializers.ModelSerializer):
    # User fields — readable & writable
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.EmailField(source='user.email', allow_blank=True, required=False)
    dob = serializers.DateField(source='user.dob', required=False, allow_null=True)
    gender = serializers.CharField(source='user.gender', required=False, allow_null=True)

    class Meta:
        model = doctor
        fields = [
            "id",
            "first_name", "last_name", "email", "dob", "gender",
            "image",
            "phone_number", "clinic_name", "clinic_phone_number",
            "house_building", "locality", "pincode", "state", "city", "country",
            "designation", "title", "degree", "specializations", "education", "about_doctor",
            "experience_years", "rating", "review_count", "remark", "is_active"
        ]

    def create(self, validated_data):
        user_data = validated_data.pop('user', {})
        user = self.context['request'].user
        for field, value in user_data.items():
            setattr(user, field, value)
        user.save()
        return doctor.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        user = instance.user
        for field, value in user_data.items():
            setattr(user, field, value)
        user.save()
        return super().update(instance, validated_data)
    



class medicine_serializer(serializers.ModelSerializer):
    class Meta:
        model = medicine
        fields = ['id', 'name', 'brand', 'power', 'form', 'description', 'is_active']
        read_only_fields = ['created_by']
        
    def create(self, validated_data):
        return medicine.objects.create(**validated_data)
    


class AppointmentMedicineSerializer(serializers.ModelSerializer):
    Appointment_details = AppointmentSerializer(source = "appointment",  read_only=True)
    medicine_details = medicine_serializer(source="medicine", read_only=True)
    class Meta:
        model = Appoinment_Medicine
        fields = "__all__"
        read_only_fields = ["user", "doctor", "Appointment_details", "medicine_details"]
    depth =1


class AppointmentTreatmentStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppointmentTreatmentStep
        fields = [
            "id",
            "step_number",
            "title",
            "date",

            "description",
            "status",
            "price",
        ]
        read_only_fields = ["date"]


class AppointmentTreatmentSerializer(serializers.ModelSerializer):
    steps = AppointmentTreatmentStepSerializer(many=True)
    Appointment_details = AppointmentSerializer(source="appointment", read_only=True)
    total_price = serializers.SerializerMethodField()
    remaining_amount = serializers.SerializerMethodField()

    class Meta:
        model = AppointmentTreatment
        fields = [
            "id",
            "appointment",
            "doctor",
            "treatment",
            "created_at",
            "steps",
            "Appointment_details",
            "total_price",
            "remaining_amount",
        ]
        read_only_fields = ["doctor", "appointment"]

    def get_total_price(self, obj):
        # sum of all step prices (change filter if you only want completed steps)
        return sum(step.price for step in obj.steps.all())
    
    def get_remaining_amount(self, obj):
        # sum of all step prices (change filter if you only want completed steps)
        total_price = sum(step.price for step in obj.steps.all())
        ledger_total = obj.appointment.ledgers.aggregate(
            total=models.Sum("amount")
        )["total"] or 0
        return total_price - ledger_total

    def create(self, validated_data):
        steps_data = validated_data.pop("steps", [])
        appointment_treatment = AppointmentTreatment.objects.create(**validated_data)
        for step in steps_data:
            AppointmentTreatmentStep.objects.create(
                appointment_treatment=appointment_treatment, **step
            )
        return appointment_treatment

    def update(self, instance, validated_data):
        steps_data = validated_data.pop("steps", [])
        instance.treatment = validated_data.get("treatment", instance.treatment)
        instance.save()

        # clear old steps & recreate (simple way)
        instance.steps.all().delete()
        for step in steps_data:
            AppointmentTreatmentStep.objects.create(
                appointment_treatment=instance, **step
            )
        return instance
    
    
class AppointmentDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppointmentDocument
        fields = "__all__"
        read_only_fields = ["uploaded_by", "uploaded_at"]



        
class LabSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lab
        fields = "__all__"


class LabWorkSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = LabWork
        fields = "__all__"


class OfferSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  # show username in API

    class Meta:
        model = Offer
        fields = "__all__"
        read_only_fields = ["user", "created_at", "updated_at"]



class InventoryProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryProduct
        fields = "__all__"
        read_only_fields = ["created_at", "updated_at"]


        
class AppointmentLedgerSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppointmentLedger
        fields = ["id", "appointment", "title", "amount", "date"]




class DoctorEarningSerializer(serializers.Serializer):
    appointment_id = serializers.IntegerField()
    patient = serializers.CharField()
    doctor = serializers.CharField()
    date = serializers.DateTimeField()
    total_price = serializers.DecimalField(max_digits=12, decimal_places=2)
    received_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    pending_amount = serializers.DecimalField(max_digits=12, decimal_places=2)



    
class DoctorLeaveSerializer(serializers.ModelSerializer):
    doctor_details = doctor_serializer(source = "doctor", read_only = True)
    class Meta:
        model = DoctorLeave
        fields = ['id', 'doctor', 'leave_date', 'doctor_details']
        read_only_fields = ['doctor']  
    
    
    
    def validate(self, data):
        request_user = self.context['request'].user
        try:
            doctor_instance = doctor.objects.get(user=request_user)
        except doctor.DoesNotExist:
            raise serializers.ValidationError("You are not registered as a doctor.")
        
        leave_date = data['leave_date']
        
        if DoctorLeave.objects.filter(doctor=doctor_instance, leave_date=leave_date).exists():
            raise serializers.ValidationError({
                "leave_date": "You already marked this date as leave."
            })
        
        return data



from masters.serializers import slot_serializer

class DoctorAvailabilitySerializer(serializers.ModelSerializer):
    slot = slot_serializer()

    class Meta:
        model = DoctorAvailability
        fields = ['id', 'day', 'slot', 'is_active']



class DoctorAvailabilityBulkSerializer(serializers.Serializer):
    slots = serializers.ListField(
        child=serializers.DictField()  
    )

    def create(self, validated_data):
        
        from doctor.models import doctor
        slots_data = validated_data['slots']
        try:
            doctor_instance = doctor.objects.get(user=self.request.user)
        except doctor.DoesNotExist:
            raise serializers.ValidationError("You are not registered as a doctor.")
     
        objs = []
        for day_slots in slots_data:
            day = day_slots['day']
            slot_ids = day_slots['slot_ids']

            # validate slots exist
            from masters.models import slot  # adjust import
            valid_slots = set(slot.objects.filter(id__in=slot_ids).values_list("id", flat=True))
            missing = set(slot_ids) - valid_slots
            if missing:
                raise serializers.ValidationError({"slot_ids": f"Invalid slot_ids: {list(missing)}"})

            for slot_id in slot_ids:
                objs.append(
                    DoctorAvailability(
                        doctor=doctor_instance,
                        day=day,
                        slot_id=slot_id,
                        is_active=True
                    )
                )

        # Remove old slots for this doctor
        DoctorAvailability.objects.filter(doctor=doctor_instance).delete()

        return DoctorAvailability.objects.bulk_create(objs)
