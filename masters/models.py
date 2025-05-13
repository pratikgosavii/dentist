from django.db import models

# Create your models here.






from django.db import models


from users.models import User
from django.utils.timezone import now
from datetime import datetime, timezone

import pytz
ist = pytz.timezone('Asia/Kolkata')



from users.models import User



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

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    
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

    

class enquiry(models.Model):
  
    name = models.CharField(max_length=50)
    age = models.CharField(max_length=50)
    mobile = models.CharField(max_length=50)
    treatment = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.mobile}"

