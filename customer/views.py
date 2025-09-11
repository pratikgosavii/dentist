from django.shortcuts import render

# Create your views here.




from doctor.serializer import doctor_serializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

from rest_framework.generics import CreateAPIView, ListAPIView
from .models import *


from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from rest_framework.permissions import IsAuthenticated

from .filters import *

from .serializer import *
from rest_framework import generics, permissions
from rest_framework import viewsets, status
from rest_framework.parsers import MultiPartParser, JSONParser


class customerViewSet(viewsets.ModelViewSet):

    queryset = customer.objects.filter(is_active=True)
    serializer_class = customer_serializer
    parser_classes = [MultiPartParser, JSONParser]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        customer_obj = self.get_object()
        customer_obj.is_active = False
        customer_obj.save()
        return Response({"message": "User deactivated"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def reactivate(self, request, pk=None):
        customer_obj = self.get_object()
        customer_obj.is_active = True
        customer_obj.save()
        return Response({"message": "User reactivated"}, status=status.HTTP_200_OK)


class AppointmentViewSet(viewsets.ViewSet):
    queryset = Appointment.objects.all().order_by('-created_at')
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DoctorViewSet(viewsets.ReadOnlyModelViewSet):  
    queryset = doctor.objects.all().order_by("id")
    serializer_class = doctor_serializer
    permission_classes = [permissions.AllowAny]