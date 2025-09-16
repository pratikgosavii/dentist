from rest_framework import serializers
from .models import *


class coupon_serializer(serializers.ModelSerializer):
    class Meta:
        model = coupon
        fields = '__all__'



class EnquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = enquiry
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
