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
        fields = ['name', 'city']
        widgets = {
            'city': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter area Name'}),
        }

class medicine_Form(forms.ModelForm):

    class Meta:
        model = medicine
        fields = ['name', 'brand', 'form', 'description', 'dose_time', 'meal_relation', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Medicine Name'}),
            'brand': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Brand Name'}),
            'form': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter Description'}),
            'dose_time': forms.SelectMultiple(attrs={'class': 'form-control', 'multiple': 'multiple'}),
            'meal_relation': forms.Select(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class treatment_Form(forms.ModelForm):

    class Meta:
        model = treatment
        fields = ['name', 'description', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Medicine Name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter Description'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class TreatmentStepForm(forms.ModelForm):
    class Meta:
        model = TreatmentStep
        fields = ["treatment", "step_number", "title", "default_description"]
        widgets = {
            "treatment": forms.Select(attrs={"class": "form-control"}),
            "step_number": forms.NumberInput(attrs={"class": "form-control"}),
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "default_description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
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




class enquiry_Form(forms.ModelForm):
     class Meta:
        model = enquiry
        fields = [
            'full_name', 'phone_number', 'email', 'dob', 'age', 'gender',
            'house', 'area', 'pincode', 'state', 'city', 'status', 'enquiry_type'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email ID'}),
            'dob': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'DD/MM/YYYY', 'type': 'date'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Age'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'house': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'House/Building/Apartment No.'}),
            'area': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Locality/Area/street/Sector'}),
            'pincode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pincode'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'enquiry_type': forms.Select(attrs={'class': 'form-control'}),
        }

        
class home_banner_Form(forms.ModelForm):
    class Meta:
        model = home_banner
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'discription': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),

        }


        
class HelpQuestion_Form(forms.ModelForm):
    class Meta:
        model = HelpQuestion
        fields = ["question", "answer", "for_doctor"]
        widgets = {
            "question": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter question"}
            ),
            # keep textarea hidden, only used for submitting
            "answer": forms.Textarea(attrs={"class": "form-control", "id": "summernote"}),  # hook for summernote
        }


        