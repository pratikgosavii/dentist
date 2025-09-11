from django.db import models

# Create your models here.


from masters.models import *
from users.models import User

from .models import *

from datetime import datetime

def current_time():
    return datetime.now().time()

GENDER_CHOICES = (
    ("Male", "Male"),
    ("Female", "Female"),
    ("Other", "Other"),
)

class doctor(models.Model):

    user = models.OneToOneField('users.User', on_delete=models.CASCADE, related_name="doctor")

    # Basic Info
    name = models.CharField(max_length=120)
    image = models.ImageField(upload_to="doctor_images/", blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[
        ("Male", "Male"), ("Female", "Female"), ("Other", "Other")
    ], blank=True, null=True)

    # Contact & Clinic Info
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    clinic_name = models.CharField(max_length=150, blank=True, null=True)
    clinic_phone_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    # Address
    house_building = models.CharField(max_length=120, blank=True, null=True)
    locality = models.CharField(max_length=120, blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)
    state = models.CharField(max_length=120, blank=True, null=True)
    city = models.CharField(max_length=120, blank=True, null=True)
    country = models.CharField(max_length=120, blank=True, null=True)

    # Professional Info
    designation = models.CharField(max_length=200, blank=True, null=True)   # Dentist, Orthodontist, etc.
    title = models.CharField(max_length=120, blank=True, null=True)         # Dr., Prof., etc.
    degree = models.CharField(max_length=120, blank=True, null=True)        # MDS, BDS, etc.
    specializations = models.TextField(blank=True, null=True)               # Store as comma-separated or JSON
    education = models.TextField(blank=True, null=True)                     # Education history
    about_doctor = models.TextField(blank=True, null=True)

    # Experience & Ratings
    experience_years = models.PositiveIntegerField(blank=True, null=True)   # 25+ years
    rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    review_count = models.PositiveIntegerField(default=0)

    remark = models.CharField(max_length=120, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
    
    
DAYS_OF_WEEK = (
    ("Mon", "Monday"),
    ("Tue", "Tuesday"),
    ("Wed", "Wednesday"),
    ("Thu", "Thursday"),
    ("Fri", "Friday"),
    ("Sat", "Saturday"),
    ("Sun", "Sunday"),
)

# Clinic model
class Clinic(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.CharField(max_length=10)
    consultation_fee = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name


# Availability model
class DoctorAvailability(models.Model):
    doctor = models.ForeignKey('doctor', on_delete=models.CASCADE, related_name='availabilities')
    
    DAY_CHOICES = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]
    
    day = models.CharField(max_length=10, choices=DAY_CHOICES)
    from_time = models.TimeField()
    to_time = models.TimeField()
    
    is_active = models.BooleanField(default=True)  # in case you want to turn off that slot
    
    def __str__(self):
        return f"{self.doctor.name} - {self.day}: {self.from_time} to {self.to_time}"
    



class video_call_history(models.Model):
    doctor = models.ForeignKey('doctor', on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)




class Appoinment_Medicine(models.Model):

    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='doctor_wdefredsasmedicines')
    medicine = models.ForeignKey('masters.medicine', on_delete=models.CASCADE, related_name='swweeq')
    doctor = models.ForeignKey('doctor', on_delete=models.CASCADE, related_name='doctor_medicines')
    appointment = models.ForeignKey('customer.Appointment', on_delete=models.CASCADE, related_name='dosdsctor_medicines')

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
    customer = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='treatments')
    appointment = models.OneToOneField('customer.Appointment', on_delete=models.CASCADE, related_name='trewreeatment')
    title = models.CharField(max_length=255)  # Example: "Crown Treatment"

    

class TreatmentStep(models.Model):
    treatment = models.ForeignKey('Treatment', on_delete=models.CASCADE, related_name='steps')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    date = models.DateField()
    status = models.CharField(max_length=50, default='Completed')  # You can later add choices
    doctor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='treatment_steps')

    class Meta:
        ordering = ['id']



