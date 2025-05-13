from django.contrib import admin

# Register your models here.

from .models import *


admin.site.register(customer)
admin.site.register(Appointment)