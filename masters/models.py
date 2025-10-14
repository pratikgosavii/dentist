from django.db import models

# Create your models here.






from django.db import models


from django.utils.timezone import now
from datetime import datetime, timezone

import pytz
ist = pytz.timezone('Asia/Kolkata')






class coupon(models.Model):

    TYPE_CHOICES = [
        ('percent', 'Percentage'),
        ('amount', 'Amount'),
    ]
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='percent')  # 👈 Add this

    code = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=500, null=True, blank=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    min_purchase = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    max_discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to='doctor_images/')
    start_date = models.DateTimeField(default=now)
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.code
    

class medicine(models.Model):

    created_by = models.ForeignKey("users.User", on_delete=models.CASCADE, blank=True, null=True)
    
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255, blank=True, null=True)
    power = models.CharField(max_length=100, blank=True, null=True)  # e.g., 'Standard', 'Extra Strong'
    form = models.CharField(max_length=100, choices=[
        ('tablet', 'Tablet'),
        ('capsule', 'Capsule'),
        ('syrup', 'Syrup'),
        ('injection', 'Injection'),
        ('ointment', 'Ointment'),
        ('drop', 'Drop'),
        ('spray', 'Spray'),
    ])
    description = models.TextField(blank=True, null=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"
    

class slot(models.Model):
  
    start  = models.TimeField()
    end    = models.TimeField()
   
    def __str__(self):
        return f"{self.start}‑{self.end}"

    

class city(models.Model):
  
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class area(models.Model):
    
    city = models.ForeignKey(city, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
        
    def __str__(self):
        return f"{self.name}"
    

STATUS_CHOICES = [
    ('Pending', 'Pending'),
    ('completed', 'Completed'),
]


GENDER_CHOICES = [
    ("Male", "Male"),
    ("Female", "Female"),
    ("Other", "Other"),
]

ENQUIRY_TYPE_CHOICES = [
    ("aligners", "Aligners"),
    ("skin_hydrafacial", "Skin/Hydrafacial"),
    ("home_visit", "Home Visit"),
]

BOOKING_TYPE_CHOICES = [
    ("self", "Booking for Yourself"),
    ("other", "Booking for Someone Else"),
]

from users.models import User


class enquiry(models.Model):
   

    

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="enquiries_user", blank=True, null=True)  
    full_name = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)

    house = models.CharField("House/Building/Apartment No.", max_length=100, blank=True, null=True)
    area = models.CharField("Locality/Area/street/Sector", max_length=150, blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    enquiry_type = models.CharField(max_length=20, choices=ENQUIRY_TYPE_CHOICES, default='Pending')
    booking_type = models.CharField(
        max_length=10,
        choices=BOOKING_TYPE_CHOICES,
        default="self"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)


class home_banner(models.Model):
    title = models.CharField(max_length=225, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='homeBanners/')
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

class treatment(models.Model):
    """
    Master treatment template (e.g., Crown Treatment, Root Canal).
    """
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return self.name


class TreatmentStep(models.Model):
    """
    Steps inside a treatment template.
    """
    treatment = models.ForeignKey(treatment, on_delete=models.CASCADE, related_name="steps", blank=True, null=True)
    step_number = models.PositiveIntegerField()
    title = models.CharField(max_length=255)
    default_description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["step_number"]
        unique_together = ("treatment", "step_number")

    def __str__(self):
        return f"{self.treatment.name} - Step {self.step_number}: {self.title}"





class HelpQuestion(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()  # stores HTML content
    for_doctor = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question
    


    
class Prescription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='prescriptions')
    title = models.CharField(max_length=200,)
    description = models.TextField(blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title
    

class PrescriptionMedicine(models.Model):
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE, related_name='medicines')
    medicine = models.ForeignKey(medicine, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=4, decimal_places=1)
    
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

    def __str__(self):
        return f"{self.medicine.name} ({self.prescription.user})"
