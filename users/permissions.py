from rest_framework.permissions import BasePermission

class IsDoctor(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_doctor

class IsDaycare(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_daycare

class IsServiceProvider(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_service_provider

class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_customer
