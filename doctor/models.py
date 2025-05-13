from django.db import models

# Create your models here.


from masters.models import *
from customer.models import *
from users.models import User
from .models import *

from datetime import datetime

def current_time():
    return datetime.now().time()

class doctor(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="doctor")
    name = models.CharField(max_length=120, unique=False)
    image = models.ImageField(upload_to='doctor_images/')
    
    house_building  = models.CharField(max_length=120,blank=True)
    locality        = models.CharField(max_length=120,blank=True)
    pincode         = models.CharField(max_length=10,blank=True)
    state           = models.CharField(max_length=120, blank=True)
    city            = models.CharField(max_length=120, blank=True)
    country         = models.CharField(max_length=120, blank=True)

    about_doctor = models.CharField(max_length=500, unique=False)
    mobile_no = models.IntegerField(null = True, blank = True)
    experience = models.IntegerField(null = True, blank = True)
    title = models.CharField(max_length=120, unique=False)
    degree = models.CharField(max_length=120, unique=False)
    rating = models.DecimalField(max_digits=3, decimal_places=1, null = True, blank = True)
    remark = models.CharField(max_length=120, unique=False, null = True, blank = True)
    is_active = models.BooleanField(default = True)
        
    available_from = models.DateField(null=True, blank=True)
    available_to = models.DateField(null=True, blank=True)

    
    def __str__(self):
        return self.name
    
    


class video_call_history(models.Model):
    doctor = models.ForeignKey(doctor, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)



from customer.models import *

class Appoinment_Medicine(models.Model):

    customer = models.ForeignKey(customer, on_delete=models.CASCADE)
    medicine = models.ForeignKey(medicine, on_delete=models.CASCADE)
    doctor = models.ForeignKey(doctor, on_delete=models.CASCADE, related_name='doctor_medicines')
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)

    quantity = models.DecimalField(max_digits=4, decimal_places=1)  # Add max_digits also
    
    dose_time = models.CharField(
        max_length=20,
        choices=[
            ('morning', 'Morning'),
            ('afternoon', 'Afternoon'),
            ('night', 'Night'),
        ]
    )

    dose = models.CharField(
        max_length=20,
        choices=[
            ('half', 'Half'),
            ('1', '1'),
            ('5 ml', '5 ml'),
            ('10 ml', '10 ml'),
            ('15 ml', '15 ml'),
            ('20 ml', '20 ml'),
        ]
    )

    meal_relation = models.CharField(
        max_length=30,
        choices=[
            ('before_breakfast', 'Before Breakfast'),
            ('after_breakfast', 'After Breakfast'),
            ('before_lunch', 'Before Lunch'),
            ('after_lunch', 'After Lunch'),
            ('before_dinner', 'Before Dinner'),
            ('after_dinner', 'After Dinner'),
        ]
    )

    duration_in_days = models.PositiveIntegerField(default=1)
    instructions = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.medicine.name} ({self.medicine.strength})"
    



class Treatment(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='treatments')
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='treatment')
    title = models.CharField(max_length=255)  # Example: "Crown Treatment"

    

class TreatmentStep(models.Model):
    treatment = models.ForeignKey(Treatment, on_delete=models.CASCADE, related_name='steps')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    date = models.DateField()
    status = models.CharField(max_length=50, default='Completed')  # You can later add choices
    doctor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='treatment_steps')

    class Meta:
        ordering = ['id']
