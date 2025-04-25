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


urlpatterns = [



    # path('add-doctor/', add_doctor, name='add_doctor'),
    # path('update-doctor/<int:doctor_id>/', update_doctor, name='update_doctor'),
    # path('list-doctor/', list_doctor, name='list_doctor'),
    # path('delete-doctor/<int:doctor_id>/', delete_doctor, name='delete_doctor'),


] + router.urls 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)