from django.urls import path

from .views import *

from django.conf import settings
from django.conf.urls.static import static

from rest_framework.routers import DefaultRouter
from django.urls import path, include

router = DefaultRouter()
router.register(r'customer', customerViewSet, basename='customer')
router.register(r'appointment', AppointmentViewSet, basename='appointment')
router.register(r'doctors-list', DoctorViewSet, basename='doctors-list')

router.register(r'support/tickets', SupportTicketViewSet, basename='support-ticket')

appointment_treatment_list = AppointmentTreatmentViewSet.as_view({
    'get': 'list',
})


urlpatterns = [

    path(
            "appointments/<int:appointment_id>/medicines/",
            AppointmentMedicineListView.as_view(),
            name="appointment-medicine-list",
        ),

    path("doctors/<int:doctor_id>/availability/", DoctorWeeklyAvailabilityAPIView.as_view(), name="doctor-weekly-availability"),



    path("appointments/<int:appointment_id>/treatments/", appointment_treatment_list, name="appointment-treatment-list"),



] + router.urls 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)