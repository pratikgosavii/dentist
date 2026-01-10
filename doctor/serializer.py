
from rest_framework import serializers
from django.contrib.auth.hashers import make_password


from .models import *
from customer.serializer import *
from rest_framework import serializers
from users.serializer import UserProfileSerializer
from datetime import date



from masters.serializers import slot_serializer

class DoctorAvailabilitySerializer(serializers.ModelSerializer):
    slot = slot_serializer()

    class Meta:
        model = DoctorAvailability
        fields = ['id', 'day', 'slot', 'is_active']


class doctor_serializer(serializers.ModelSerializer):

    availabilities = DoctorAvailabilitySerializer(many=True, read_only=True)
    is_all_details_available = serializers.SerializerMethodField()
    is_availabilities_details = serializers.SerializerMethodField()

    # User fields — readable & writable
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.EmailField(source='user.email', allow_blank=True, required=False)
    dob = serializers.DateField(source='user.dob', required=False, allow_null=True)
    profile_photo = serializers.ImageField(source='user.profile_photo', required=False, allow_null=True)
    gender = serializers.CharField(source='user.gender', required=False, allow_null=True)
    users_details = UserProfileSerializer(source = 'user', read_only = True)
    
    offers = serializers.SerializerMethodField()
    
    average_rating = serializers.SerializerMethodField()   
    review_count = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()  # optional, list of reviews


    class Meta:
        model = doctor
        fields = [
            "id",
            "first_name", "last_name", "email", "dob", "gender", "profile_photo",
            "users_details",
            "clinic_name", "clinic_phone_number", "clinic_consultation_fees", "clinic_image", "clinic_logo",
            "street_address", "pincode", "state", "city", "country",
            "title", "degree", "specializations", "education", "about_doctor", "latitude", "longitude",
            "experience_years", "rating", "review_count", "remark", "is_active", "offers", "is_all_details_available", "is_availabilities_details", 'availabilities',

            "review_count", "average_rating", "reviews",

        ]
        read_only_fields = ["is_active", "offers"]

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
    
    def get_offers(self, obj):
        """Return only active offers for this doctor"""
        today = date.today()
        offers = Offer.objects.filter(
            user=obj.user, valid_to__lte=today
        )
        return OfferSerializer(offers, many=True).data

    def get_is_all_details_available(self, obj):
        required_doctor_fields = [
            "clinic_name", "clinic_consultation_fees",
            "clinic_phone_number", "street_address",
            "state", "city", "country", "title", "degree",
            "specializations", "education", "about_doctor", "experience_years",
        ]
        required_user_fields = [
             "first_name", "last_name", 
        ]

        # check doctor fields
        for field in required_doctor_fields:
            value = getattr(obj, field, None)
            if value in [None, "", []]:
                return False

        # check user fields
        for field in required_user_fields:
            value = getattr(obj.user, field, None)
            if value in [None, "", []]:
                return False

      
        return True


    def get_is_availabilities_details(self, obj):

        # ✅ Check if doctor has all 7 days of active availability
        days_present = (
            obj.availabilities
            .filter(is_active=True)
            .values_list("day", flat=True)
            .distinct()
        )

        required_days = {
            'Monday', 'Tuesday', 'Wednesday',
            'Thursday', 'Friday', 'Saturday', 'Sunday'
        }

        if not required_days.issubset(set(days_present)):
            return False

        return True
        
    def get_average_rating(self, obj):
        from django.db.models import Avg
        avg = obj.appointments_doctor.filter(review__isnull=False).aggregate(avg=Avg('review__rating'))['avg']
        return round(avg or 0, 1)

    def get_review_count(self, obj):
        return obj.appointments_doctor.filter(review__isnull=False).count()

    def get_reviews(self, obj):
        reviews = obj.appointments_doctor.filter(review__isnull=False).select_related('review')
        return [
            {
                "appointment_id": r.id,
                "rating": r.review.rating,
                "comment": r.review.comment,
                "created_at": r.review.created_at,
                "customer": {
                    "id": r.user.id,
                    "name": r.user.first_name + " " + r.user.last_name
                }
            }
            for r in reviews
        ]
    


class medicine_serializer(serializers.ModelSerializer):
    class Meta:
        model = medicine
        fields = ['id', 'name', 'brand', 'form', 'description', 'dose_time', 'meal_relation', 'is_active']
        read_only_fields = ['created_by']
        
    def create(self, validated_data):
        return medicine.objects.create(**validated_data)
    

from customer.serializer import AppointmentSerializer

class AppointmentMedicineSerializer(serializers.ModelSerializer):
    medicine_details = medicine_serializer(source="medicine", read_only=True)
    
    DOSE_TIME_CHOICES = ['morning', 'afternoon', 'night']
    
    def validate_dose_time(self, value):
        """Validate that dose_time contains only valid choices"""
        if not isinstance(value, list):
            raise serializers.ValidationError("dose_time must be a list.")
        if not value:
            raise serializers.ValidationError("At least one dose_time must be selected.")
        invalid_choices = [choice for choice in value if choice not in self.DOSE_TIME_CHOICES]
        if invalid_choices:
            raise serializers.ValidationError(
                f"Invalid choices: {invalid_choices}. Valid choices are: {self.DOSE_TIME_CHOICES}"
            )
        return value
    
    class Meta:
        model = Appoinment_Medicine
        fields = "__all__"
        read_only_fields = ["user", "doctor", "medicine_details"]


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
        # date is now writable and comes from API

from masters.serializers import TreatmentSerializer

class AppointmentTreatmentSerializer(serializers.ModelSerializer):
    steps = AppointmentTreatmentStepSerializer(many=True)
    total_price = serializers.SerializerMethodField()
    treatment_details = TreatmentSerializer(source="treatment", read_only=True)
    doctor_details = doctor_serializer(source = "doctor", read_only=True)
    class Meta:
        model = AppointmentTreatment
        fields = [
            "id",
            "appointment",
            "doctor",
            "doctor_details",
            "treatment",
            "treatment_details",
            "created_at",
            "steps",
            "total_price",
        ]
        read_only_fields = ["doctor", "appointment", "treatment_details"]

    def get_total_price(self, obj):
        # sum of all step prices (change filter if you only want completed steps)
        return sum(step.price for step in obj.steps.all())
    

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


        

from functools import lru_cache

class AppointmentLedgerSerializer(serializers.ModelSerializer):
    total_amount = serializers.SerializerMethodField()
    ledger_paid = serializers.SerializerMethodField()
    remaining_amount = serializers.SerializerMethodField()

    class Meta:
        model = AppointmentLedger
        fields = [
            "id",
            "appointment",
            "title",
            "amount",
            "date",
            "total_amount",
            "ledger_paid",
            "remaining_amount",
        ]

    # Cache totals per appointment so multiple ledgers don't trigger multiple queries
    @lru_cache(maxsize=None)
    def _get_totals(self, appointment_id):
        total_amount = (
            AppointmentTreatmentStep.objects
            .filter(appointment_treatment__appointment_id=appointment_id)
            .aggregate(total=Sum("price"))["total"]
            or 0
        )
        ledger_paid = (
            AppointmentLedger.objects
            .filter(appointment_id=appointment_id)
            .aggregate(total=Sum("amount"))["total"]
            or 0
        )
        return total_amount, ledger_paid

    def get_total_amount(self, obj):
        total, _ = self._get_totals(obj.appointment_id)
        return total

    def get_ledger_paid(self, obj):
        _, paid = self._get_totals(obj.appointment_id)
        return paid

    def get_remaining_amount(self, obj):
        total, paid = self._get_totals(obj.appointment_id)
        return total - paid


        
class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ["id", "title", "amount", "date"]




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

        # 1️⃣ Check if leave already exists
        if DoctorLeave.objects.filter(doctor=doctor_instance, leave_date=leave_date).exists():
            raise serializers.ValidationError({
                "leave_date": "You already marked this date as leave."
            })

        # 2️⃣ Check if any appointment exists on this date
        if Appointment.objects.filter(doctor=doctor_instance, date=leave_date).exists():
            raise serializers.ValidationError({
                "leave_date": "You cannot mark leave on this date because there are existing appointments."
            })

        return data




class DoctorAvailabilityBulkSerializer(serializers.Serializer):
    slots = serializers.ListField(
        child=serializers.DictField()  
    )

    def create(self, validated_data):
        
        from doctor.models import doctor
        slots_data = validated_data['slots']

        request = self.context.get("request")

        try:
            doctor_instance = doctor.objects.get(user=request.user)
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


class DoctorAppointmentSerializer(serializers.ModelSerializer):
    slot_details = slot_serializer(source="slot", read_only=True)
    customer_details = UserProfileSerializer(source="user", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    # ✅ add SerializerMethodFields here
    total_amount = serializers.SerializerMethodField()
    ledger_paid = serializers.SerializerMethodField()
    remaining_amount = serializers.SerializerMethodField()

    # 💊 Related fields
    treatments = serializers.SerializerMethodField()
    medicines = serializers.SerializerMethodField()
    documents = serializers.SerializerMethodField()
    ledgers = serializers.SerializerMethodField()


    class Meta:
        model = Appointment
        fields = [
        "id", "user", "slot_details", "appointment_type", "status", "status_display",
        "date", "slot", "customer_details", "concern", "created_at",
        "total_amount", "ledger_paid", "remaining_amount",
        "treatments", "medicines", "documents", "ledgers",
    ]
        read_only_fields = ["created_at", "customer_details"]

    def validate_date(self, value):
        if value < date.today():
            raise serializers.ValidationError("Appointment date cannot be in the past.")
        return value
    

    def get_treatments(self, obj):
        from doctor.serializer import AppointmentTreatmentSerializer
        return AppointmentTreatmentSerializer(obj.treatments.all(), many=True).data

    def get_medicines(self, obj):
        from doctor.serializer import AppointmentMedicineSerializer
        return AppointmentMedicineSerializer(obj.dosdsctor_medicines.all(), many=True).data

    def get_documents(self, obj):
        from doctor.serializer import AppointmentDocumentSerializer
        return AppointmentDocumentSerializer(obj.documents.all(), many=True).data

    def get_ledgers(self, obj):
        from doctor.serializer import AppointmentLedgerSerializer

        return AppointmentLedgerSerializer(obj.ledgers.all(), many=True).data

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



class ToothSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tooth
        fields = ["id", "number", "status"]