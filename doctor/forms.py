from django import forms

from .models import *
from django.contrib.admin.widgets import  AdminDateWidget, AdminTimeWidget, AdminSplitDateTime


class doctor_Form(forms.ModelForm):
    class Meta:
        model = doctor
        fields = '__all__'
        widgets = {
           
            'name': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'name'
            }),
           
            'degree': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'degree'
            }),

            'title': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'title'
            }),

            'address': forms.Textarea(attrs={'class': 'form-control', 'id': 'address', 'rows': 3}), 

            'mobile_no': forms.NumberInput(attrs={
                'class': 'form-control', 'id': 'mobile_no'
            }),

            'experience': forms.NumberInput(attrs={
                'class': 'form-control', 'id': 'experience'
            }),
            
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            
            'remark': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'remark'
            }),
            
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'is_active'}),
            
        }



    def save(self, commit=True):
        # Create a new User instance
        doctor_instance = super().save(commit=False)  # Get the doctor instance without saving it yet

        if not doctor_instance.user:  
            # If the doctor doesn't have a user, create a new one
            user = User.objects.create(username=self.cleaned_data['name'], is_doctor=True)
            user.set_password("defaultpassword")  # Hash the password
            user.save()
            doctor_instance.user = user  
        else:
            # If user already exists, update username
            doctor_instance.user.username = self.cleaned_data['name']
            doctor_instance.user.save()

        if commit:
            doctor_instance.save()

        return doctor_instance






class coupon_Form(forms.ModelForm):
    class Meta:
        model = coupon
        fields = '__all__'  # Include all fields
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Coupon Code'}),
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




class testimonials_Form(forms.ModelForm):
    class Meta:
        model = testimonials
        fields = '__all__'
        widgets = {
           
            'name': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'name'
            }),

            'rating': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
          
            'description': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'price'
            }),

        }



