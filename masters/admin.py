from django.contrib import admin

# Register your models here.


from .models import *

admin.site.register(medicine)
admin.site.register(area)
admin.site.register(city)
admin.site.register(PrescriptionMedicine)
admin.site.register(Prescription)