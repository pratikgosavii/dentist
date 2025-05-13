from django import forms

from .models import *
from django.contrib.admin.widgets import  AdminDateWidget, AdminTimeWidget, AdminSplitDateTime


class coupon_Form(forms.ModelForm):
    class Meta:
        model = coupon
        fields = '__all__'  # Include all fields
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Coupon Code'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter Coupon Code'}),
            'discount_percentage': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'discount_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'min_purchase': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'max_discount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class city_Form(forms.ModelForm):

    class Meta:
        model = city
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter city Name'}),
        }

class area_Form(forms.ModelForm):

    class Meta:
        model = area
        fields = ['name']
        widgets = {
            'city': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter area Name'}),
        }

class medicine_Form(forms.ModelForm):

    class Meta:
        model = medicine
        fields = ['name', 'brand', 'power', 'form', 'description', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Medicine Name'}),
            'brand': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Brand Name'}),
            'power': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 500mg, Extra Strong'}),
            'form': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter Description'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class slot_Form(forms.ModelForm):

    class Meta:
        model = slot
        fields = ['start', 'end']
        widgets = {
            "start": forms.TimeInput(              # HH:MM picker
                format="%H:%M",
                attrs={
                    "class": "form-control",
                    "type": "time",
                },
            ),
            "end": forms.TimeInput(
                format="%H:%M",
                attrs={
                    "class": "form-control",
                    "type": "time",
                },
            ),
        }