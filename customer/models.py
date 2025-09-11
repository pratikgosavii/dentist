from django.db import models

# Create your models here.


from masters.models import *
from users.models import User
from .models import *

from datetime import datetime
from datetime import date
from users.models import User



def current_time():
    return datetime.now().time()

class customer(models.Model):

    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="customer")
    dob = models.DateField()
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    is_active = models.BooleanField(default=True)

    @property
    def age(self):
        today = date.today()
        return today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))

    def __str__(self):
        return self.user.first_name
    


GENDER_CHOICES = [
    ('Male', 'Male'),
    ('Female', 'Female'),
]

APPOINTMENT_TYPE_CHOICES = [
    ('In Person', 'In Person'),
    ('Over a Call', 'Over a Call'),
]

class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="appointments")
    appointment_type = models.CharField(max_length=20, choices=APPOINTMENT_TYPE_CHOICES, default="In Person")

    # Appointment details
    date = models.DateField()
    time = models.TimeField()

    # Patient details
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    dob = models.DateField()
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)

    concern = models.TextField(blank=True, null=True)

    # Meta info
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Appointment for {self.full_name} on {self.date} at {self.time}"