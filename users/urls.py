from django.urls import path

from .views import *

from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'profile', UserProfileViewSet, basename='user-profile')

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path('login-admin/', login_admin, name='login_admin'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('update-user/', UserUpdateView.as_view(), name='UserUpdateView'),
    path('get-user/', UsergetView.as_view(), name='UsergetView'),
    path('reset-password/', ResetPasswordView.as_view(), name='ResetPasswordView'),
    path('logout/', logout_page, name='logout'),

    path('delete-account/', delete_user, name='delete_account'),

    path('dentist_list/', dentist_list, name='dentist_list'),
    path('user_list/', user_list, name='user_list'),
] + router.urls
