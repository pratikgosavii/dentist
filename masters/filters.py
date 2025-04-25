import django_filters
from .models import *


class couponFilter(django_filters.FilterSet):
    class Meta:
        model = coupon
        exclude = ['image']  # ⛔ Exclude unsupported field

