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
router.register("appointment-documents", AppointmentDocumentViewSet, basename="appointment-document")
router.register('appointments', DoctorAppointmentViewSet, basename="doctor-appointments")

router.register('labs', LabViewSet, basename="lab")
router.register('lab-works', LabWorkViewSet, basename="labwork")

router.register(r'offers', OfferViewSet, basename='offer')

router.register(r'inventory', InventoryProductViewSet, basename='inventory')

router.register(r'appointment-ledgers', AppointmentLedgerViewSet, basename='appointment-ledger')

router.register(r'expense', ExpenseViewSet, basename='expense')

router.register(r'doctor-leaves', DoctorLeaveViewSet, basename='doctor-leaves')

appointment_treatment_list = AppointmentTreatmentViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

appointment_treatment_detail = AppointmentTreatmentViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy',
})


urlpatterns = [


    path("list-treatments/", TreatmentAPIView.as_view(), name="list_treatement"),
    
    path("list-appointment/", AppointmentsListAPIView.as_view(), name="list-customer-appointment"),
    path("list-appointment/<int:appointment_id>/", AppointmentsListAPIView.as_view(), name="detail-customer-appointment"),
    
    path("create-customer/", DoctorVerifyCustomerOTP.as_view(), name="DoctorVerifyCustomerOTP"),

    path("appointments/<int:appointment_id>/treatments/", appointment_treatment_list, name="appointment-treatment-list"),
    path("appointments/<int:appointment_id>/treatments/<int:pk>/", appointment_treatment_detail, name="appointment-treatment-detail" ),
    
    path('report/', DoctorReportAPIView.as_view(), name='doctor-report-api'),
    
    path('list-patient/', list_patient.as_view(), name='list_patient'),
    
    path('availability/', DoctorAvailabilityView.as_view()),   # POST



] + router.urls 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)