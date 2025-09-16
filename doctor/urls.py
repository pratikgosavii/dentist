from django.urls import path

from .views import *

from django.conf import settings
from django.conf.urls.static import static

from rest_framework.routers import DefaultRouter
from .views import DoctorViewSet
from django.urls import path, include

router = DefaultRouter()
router.register('doctors', DoctorViewSet, basename='doctor')
router.register('doctor-medicine', DoctorMedicineViewSet, basename='pet-test-booking')
router.register('appointment-medicine', AppointmentMedicineViewSet, basename='AppointmentMedicineViewSet')
router.register(
    r"appointments/(?P<appointment_id>\d+)/treatments",
    AppointmentTreatmentViewSet,
    basename="appointment-treatments"
)


urlpatterns = [


    path("list-treatments/", TreatmentAPIView.as_view(), name="list_treatement"),
    path("list-appointment/", AppointmentsListAPIView.as_view(), name="list-customer-appointment"),


    # path(
    #     "appointments/<int:appointment_id>/add-treatment/<int:treatment_id>/",
    #     AppointmentTreatmentCreateAPIView.as_view(),
    #     name="appointment-add-treatment",
    # ),

    # path('add-doctor/', add_doctor, name='add_doctor'),
    # path('update-doctor/<int:doctor_id>/', update_doctor, name='update_doctor'),
    # path('list-doctor/', list_doctor, name='list_doctor'),
    # path('delete-doctor/<int:doctor_id>/', delete_doctor, name='delete_doctor'),


] + router.urls 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)