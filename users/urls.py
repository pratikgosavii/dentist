from django.urls import path

from .views import *

from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'profile', UserProfileViewSet, basename='user-profile')

urlpatterns = [
    # OTP endpoints
    path('send-otp/', SendOTPView.as_view(), name='send_otp'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
    
    # Authentication endpoints
    path('login/', LoginAPIView.as_view(), name='login'),
    path('login-admin/', login_admin, name='login_admin'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('update-user/', UserUpdateView.as_view(), name='UserUpdateView'),
    path('get-user/', UsergetView.as_view(), name='UsergetView'),
    path('reset-password/', ResetPasswordView.as_view(), name='ResetPasswordView'),
    path('logout/', logout_page, name='logout'),
    path('register-device-token/', RegisterDeviceTokenAPIView.as_view(), name='RegisterDeviceTokenAPIView'),

    # Notifications (same API for doctor and customer — returns notifications for logged-in user)
    path('notifications/', NotificationListAPIView.as_view(), name='notification_list'),
    path('notifications/<int:pk>/mark-read/', MarkNotificationReadAPIView.as_view(), name='notification_mark_read'),

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
