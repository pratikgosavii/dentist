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

urlpatterns = [



] + router.urls 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)