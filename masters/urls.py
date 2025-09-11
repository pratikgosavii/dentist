from django.urls import path

from .views import *

from django.conf import settings
from django.conf.urls.static import static




from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('enquiries', EnquiryViewSet, basename='enquiry')


urlpatterns = [

    path('add-coupon/', add_coupon, name='add_coupon'),
    path('update-coupon/<coupon_id>', update_coupon, name='update_coupon'),
    path('delete-coupon/<coupon_id>', delete_coupon, name='delete_coupon'),
    path('list-coupon/', list_coupon, name='list_coupon'),
    path('get-coupon/', get_coupon.as_view(), name='get_coupon'),
    
    path('add-medicine/', add_medicine, name='add_medicine'),
    path('update-medicine/<medicine_id>', update_medicine, name='update_medicine'),
    path('delete-medicine/<medicine_id>', delete_medicine, name='delete_medicine'),
    path('list-medicine/', list_medicine, name='list_medicine'),

    path('add-slot/', add_slot, name='add_slot'),
    path('update-slot/<slot_id>', update_slot, name='update_slot'),
    path('delete-slot/<slot_id>', delete_slot, name='delete_slot'),
    path('list-slot/', list_slot, name='list_slot'),

    path('add-city/', add_city, name='add_city'),
    path('update-city/<city_id>', update_city, name='update_city'),
    path('delete-city/<city_id>', delete_city, name='delete_city'),
    path('list-city/', list_city, name='list_city'),

    path('add-area/', add_area, name='add_area'),
    path('update-area/<area_id>', update_area, name='update_area'),
    path('delete-area/<area_id>', delete_area, name='delete_area'),
    path('list-area/', list_area, name='list_area'),

    path('update-enquiry/<enquiry_id>', update_enquiry, name='update_enquiry'),
    path('delete-enquiry/<enquiry_id>', delete_enquiry, name='delete_enquiry'),
    path('list-enquiry/', list_enquiry, name='list_enquiry'),
    
    path('list-apppoinments/', list_apppoinments, name='list_apppoinments'),
    

    ]  + router.urls

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)