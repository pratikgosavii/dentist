from django.contrib import admin

# Register your models here.


from .models import *

admin.site.register(doctor)
# admin.site.register(Treatment)
admin.site.register(TreatmentStep)
admin.site.register(Tooth)
admin.site.register(AppointmentLedger)
