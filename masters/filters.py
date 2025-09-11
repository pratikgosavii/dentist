import django_filters
from .models import *


class couponFilter(django_filters.FilterSet):
    class Meta:
        model = coupon
        exclude = ['image']  # ⛔ Exclude unsupported field

import django_filters
from django import forms
from customer.models import *
from doctor.models import *

import django_filters
from django import forms
from .models import enquiry

class EnquiryFilter(django_filters.FilterSet):
    user = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        label="User",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    full_name = django_filters.CharFilter(
        lookup_expr='icontains',
        label="Full name",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter full name'})
    )
    phone_number = django_filters.CharFilter(
        lookup_expr='icontains',
        label="Phone number",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone number'})
    )
    city = django_filters.CharFilter(
        lookup_expr='icontains',
        label="City",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter city'})
    )
    status = django_filters.ChoiceFilter(
        choices=[('Pending', 'Pending'), ('Approved', 'Approved')],
        label="Status",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    enquiry_type = django_filters.CharFilter(
        lookup_expr='icontains',
        label="Enquiry Type",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter enquiry type'})
    )
    created_at = django_filters.DateFromToRangeFilter(
        label="Date Range",
        widget=django_filters.widgets.RangeWidget(
            attrs={'type': 'date', 'class': 'form-control'}
        )
    )

    class Meta:
        model = enquiry
        fields = ['user', 'full_name', 'phone_number', 'city', 'status', 'enquiry_type', 'created_at']


class AppointmentFilter(django_filters.FilterSet):
    user = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        label="User",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    full_name = django_filters.CharFilter(
        lookup_expr='icontains',
        label="Full Name",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter full name'})
    )

    phone_number = django_filters.CharFilter(
        lookup_expr='icontains',
        label="Phone Number",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone number'})
    )

    gender = django_filters.ChoiceFilter(
        choices=[('Male', 'Male'), ('Female', 'Female')],
        label="Gender",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    appointment_type = django_filters.ChoiceFilter(
        choices=[('In Person', 'In Person'), ('Over a Call', 'Over a Call')],
        label="Appointment Type",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    date = django_filters.DateFromToRangeFilter(
        label="Date Range",
        widget=django_filters.widgets.RangeWidget(attrs={'type': 'date', 'class': 'form-control'})
    )

    class Meta:
        model = Appointment
        fields = ['user', 'full_name', 'phone_number', 'gender', 'appointment_type', 'date']