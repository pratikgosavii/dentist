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
    

class Appointment(models.Model):

    doctor   = models.ForeignKey("doctor.doctor", on_delete=models.CASCADE, related_name="appointments")
    customer  = models.ForeignKey("customer.customer", on_delete=models.CASCADE, related_name="sdsd",)
    date     = models.DateField()
    slot     = models.ForeignKey(slot, on_delete=models.PROTECT, related_name="sdssdsdd")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("doctor", "date", "slot")  # no double‑booking
        ordering        = ["date", "slot__start"]

    def __str__(self):
        return f"{self.customer} with {self.doctor} on {self.date} @ {self.slot.start}"

    