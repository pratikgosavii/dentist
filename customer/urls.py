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

router.register(r"treatments", customer_treatment_list, basename="customer-treatments")

router.register(r"reviews", ReviewViewSet, basename="review")


urlpatterns = [

    path(
            "appointments/<int:appointment_id>/medicines/",
            AppointmentMedicineListView.as_view(),
            name="appointment-medicine-list",
        ),

    path("doctors/<int:doctor_id>/availability/", DoctorWeeklyAvailabilityAPIView.as_view(), name="doctor-weekly-availability"),
    
    path("appointment/document-list/", AppointmentDocumentListAPIView.as_view(), name="appointment-document-list"),

    path("my-doctors/", MyDoctorsAPIView.as_view(), name="my-doctors"),

    path("nearby/doctors/", NearbyDoctorsAPIView.as_view(), name="doctor-nearby"),


] + router.urls 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)