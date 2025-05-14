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



