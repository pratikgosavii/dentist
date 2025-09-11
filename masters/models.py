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
    ("home_visit", "Home Visit"),
    ("aligners", "Aligners"),
    ("skin_hydrafacial", "Skin/Hydrafacial"),
]

from users.models import User


class enquiry(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="enquiries_user")  
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    dob = models.DateField()
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)

    house = models.CharField("House/Building/Apartment No.", max_length=100)
    area = models.CharField("Locality/Area/street/Sector", max_length=150)
    pincode = models.CharField(max_length=10)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    enquiry_type = models.CharField(max_length=20, choices=ENQUIRY_TYPE_CHOICES, default='Pending')

    created_at = models.DateTimeField(auto_now_add=True)

