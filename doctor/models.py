from django.db import models

# Create your models here.


from masters.models import *
from users.models import User
from .models import *

from datetime import datetime

def current_time():
    return datetime.now().time()

class doctor(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
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
        
    available_from = models.TimeField(default=current_time)  # ✅ GOOD
    available_to = models.TimeField(default=current_time)  

    
    def __str__(self):
        return self.name
    
    


class video_call_history(models.Model):
    doctor = models.ForeignKey(doctor, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


