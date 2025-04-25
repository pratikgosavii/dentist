from django.shortcuts import render

# Create your views here.




from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

from rest_framework.generics import CreateAPIView, ListAPIView


from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from rest_framework.permissions import IsAuthenticated

from doctor.filters import *



from .serializer import *
from users.permissions import *

from rest_framework import generics, permissions
from rest_framework import viewsets, status
from rest_framework.parsers import MultiPartParser, JSONParser


class DoctorViewSet(viewsets.ModelViewSet):

    queryset = doctor.objects.filter(is_active=True)
    serializer_class = doctor_serializer
    parser_classes = [MultiPartParser, JSONParser]  # ✅ Allow both JSON and form-data

    def perform_create(self, serializer):
        print(self.request.user)
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        doctor_obj = self.get_object()
        doctor_obj.is_active = False
        doctor_obj.save()
        return Response({"message": "Doctor deactivated"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def reactivate(self, request, pk=None):
        doc = self.get_object()
        doc.is_active = True
        doc.save()
        return Response({"message": "Doctor reactivated"}, status=status.HTTP_200_OK)



from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend


from django.db.models import Q

class DoctorMedicineViewSet(viewsets.ModelViewSet):
    serializer_class = medicine_serializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return medicine.objects.filter(is_deleted=False).filter(is_active=True).filter(
            Q(created_by=self.request.user) | Q(created_by__isnull=True)  # Include superadmin and current user
        )

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = True
        instance.save()
        return Response({"detail": "Soft deleted successfully."}, status=status.HTTP_200_OK)