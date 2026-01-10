from django.urls import path

from .views import *

from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'profile', UserProfileViewSet, basename='user-profile')

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('login-admin/', login_admin, name='login_admin'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('update-user/', UserUpdateView.as_view(), name='UserUpdateView'),
    path('get-user/', UsergetView.as_view(), name='UsergetView'),
    path('reset-password/', ResetPasswordView.as_view(), name='ResetPasswordView'),
    path('logout/', logout_page, name='logout'),

    path('delete-account/', delete_user, name='delete_account'),

    path('dentist_list/', dentist_list, name='dentist_list'),
    path('export-dentist-list-excel/', export_dentist_list_excel, name='export_dentist_list_excel'),
    path('user_list/', user_list, name='user_list'),
    path('customer_list/', customer_list, name='customer_list'),
    path('export-customer-list-excel/', export_customer_list_excel, name='export_customer_list_excel'),
    path('view-doctor/<int:doctor_id>/', view_doctor_details, name='view_doctor_details'),
    path('update-user-subscription/<int:user_id>/', update_user_subscription, name='update_user_subscription'),
    path('subscription-payment-history/<int:user_id>/', subscription_payment_history, name='subscription_payment_history'),
] + router.urls
