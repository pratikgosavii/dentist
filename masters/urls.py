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
    path('get-medicine/', get_medicine.as_view(), name='get_medicine'),

    path('add-slot/', add_slot, name='add_slot'),
    path('update-slot/<slot_id>', update_slot, name='update_slot'),
    path('delete-slot/<slot_id>', delete_slot, name='delete_slot'),
    path('list-slot/', list_slot, name='list_slot'),
    path('get-slot/', get_slot.as_view(), name='get_slot'),

    path('add-city/', add_city, name='add_city'),
    path('update-city/<city_id>', update_city, name='update_city'),
    path('delete-city/<city_id>', delete_city, name='delete_city'),
    path('list-city/', list_city, name='list_city'),

    path('add-area/', add_area, name='add_area'),
    path('update-area/<area_id>', update_area, name='update_area'),
    path('delete-area/<area_id>', delete_area, name='delete_area'),
    path('list-area/', list_area, name='list_area'),

    path('add-treatment/', add_treatment, name='add_treatment'),
    path('update-treatment/<treatment_id>', update_treatment, name='update_treatment'),
    path('delete-treatment/<treatment_id>', delete_treatment, name='delete_treatment'),
    path('list-treatment/', list_treatment, name='list_treatment'),

    path('add-treatment-steps/<treatment_step_id>', add_treatment_steps, name='add_treatment_step'),
    path('update-treatment-steps/<treatment_step_id>', update_treatment_steps, name='update_treatmen_steps'),
    path('delete-treatment-steps/<treatment_step_id>', delete_treatment_steps, name='delete_treatmen_steps'),
    path('list-treatment-steps/<int:treatment_id>', list_treatment_steps, name='treatment_step_list'),

    path('update-enquiry/<enquiry_id>', update_enquiry, name='update_enquiry'),
    path('delete-enquiry/<enquiry_id>', delete_enquiry, name='delete_enquiry'),
    path('list-enquiry/', list_enquiry, name='list_enquiry'),
    
    path('list-apppoinments/', list_apppoinments, name='list_apppoinments'),

    path('add-home-banner/', add_home_banner, name='add_home_banner'),  # create or fetch list of admins
    path('update-home-banner/<home_banner_id>', update_home_banner, name='update_home_banner'),  # create or fetch list of admins
    path('list-home-banner/', list_home_banner, name='list_home_banner'),  # create or fetch list of admins
    path('delete-home-banner/<home_banner_id>', delete_home_banner, name='delete_home_banner'),  # create or fetch list of admins
    path('get-home-banner/', get_home_banner, name='get_home_banner'), 

    path('add-faq/', add_faq, name='add_faq'),  # create or fetch list of admins
    path('update-faq/<faq_id>', update_faq, name='update_faq'),  # create or fetch list of admins
    path('list-faq/', list_faq, name='list_faq'),  # create or fetch list of admins
    path('delete-faq/<faq_id>', delete_faq, name='delete_faq'),  # create or fetch list of admins
    path('get-faq/', get_faq.as_view(), name='get_home_banner'), 

    path('view-appointment-detail/<appointment_id>', view_appointment_detail, name='view_appointment_detail'),

        # urls.py
    path('admin/support-tickets/', list_support_tickets, name='list_support_tickets'),
    path('admin/support-tickets/<int:ticket_id>/', ticket_detail, name='ticket_detail'),

    ]  + router.urls

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)