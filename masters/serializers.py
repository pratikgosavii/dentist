from rest_framework import serializers
from .models import *


class coupon_serializer(serializers.ModelSerializer):
    class Meta:
        model = coupon
        fields = '__all__'


class medicine_serializer(serializers.ModelSerializer):
    class Meta:
        model = medicine
        fields = '__all__'


class slot_serializer(serializers.ModelSerializer):
    class Meta:
        model = slot
        fields = '__all__'



class EnquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = enquiry
        fields = '__all__'



class HelpQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = HelpQuestion
        fields = '__all__'





class HomeBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = home_banner
        fields = ['image'] 
    
    def get_image(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url


class TreatmentStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = TreatmentStep
        fields = ["id", "step_number", "title", "default_description"]


class TreatmentSerializer(serializers.ModelSerializer):
    steps = TreatmentStepSerializer(many=True, read_only=True)

    class Meta:
        model = treatment
        fields = ['id', 'name', 'description', 'is_active', 'steps']





class PrescriptionMedicineSerializer(serializers.ModelSerializer):
    medicine_details = medicine_serializer(read_only=True)
   
    class Meta:
        model = PrescriptionMedicine
        fields = [
            'id', 'medicine', 'medicine_details', 'quantity', 'dose', 'dose_time',
            'meal_relation', 'duration_in_days', 'instructions'
        ]


class PrescriptionSerializer(serializers.ModelSerializer):
    medicines = PrescriptionMedicineSerializer(many=True, read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Prescription
        fields = [
            'id', 'user', 'user_name', 'title', 'description', 'date', 'created_at', 'medicines'
        ]