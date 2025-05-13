from django.shortcuts import render

# Create your views here.




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
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Appointment.objects.select_related("doctor", "slot", "customer")

    def list(self, request):
        qs = self.get_queryset()
        user = request.user

        if hasattr(user, "doctor"):
            qs = qs.filter(doctor=user.doctor)
        elif hasattr(user, "customer"):
            qs = qs.filter(customer=user.customer)

        doctor_id = request.query_params.get("doctor")
        date = request.query_params.get("date")

        if doctor_id:
            qs = qs.filter(doctor_id=doctor_id)
        if date:
            qs = qs.filter(date=date)

        serializer = AppointmentSerializer(qs, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            appointment = self.get_queryset().get(pk=pk)
        except Appointment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = AppointmentSerializer(appointment)
        return Response(serializer.data)

    def create(self, request):
        user = request.user
        data = request.data.copy()

        print(user)

        if user.is_doctor:
            if not data.get("customer"):
                return Response({"error": "Customer ID is required for doctor booking."}, status=status.HTTP_400_BAD_REQUEST)
            data["doctor"] = user.doctor.id

        elif user.is_customer:
            if not data.get("doctor"):
                return Response({"error": "Doctor ID is required for customer booking."}, status=status.HTTP_400_BAD_REQUEST)
            data["customer"] = user.customer.id

        else:
            return Response({"error": "User must be a doctor or a customer."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = AppointmentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        try:
            appointment = self.get_queryset().get(pk=pk)
        except Appointment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Check permission
        user = request.user
        if hasattr(user, "doctor") and appointment.doctor != user.doctor:
            return Response({"error": "Not allowed to update this appointment."}, status=status.HTTP_403_FORBIDDEN)
        if hasattr(user, "customer") and appointment.customer != user.customer:
            return Response({"error": "Not allowed to update this appointment."}, status=status.HTTP_403_FORBIDDEN)

        serializer = AppointmentSerializer(appointment, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save(customer=appointment.customer)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        try:
            appointment = self.get_queryset().get(pk=pk)
        except Appointment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Check permission
        user = request.user
        if hasattr(user, "doctor") and appointment.doctor != user.doctor:
            return Response({"error": "Not allowed to update this appointment."}, status=status.HTTP_403_FORBIDDEN)
        if hasattr(user, "customer") and appointment.customer != user.customer:
            return Response({"error": "Not allowed to update this appointment."}, status=status.HTTP_403_FORBIDDEN)

        serializer = AppointmentSerializer(appointment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(customer=appointment.customer)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            appointment = self.get_queryset().get(pk=pk)
        except Appointment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Check permission
        user = request.user
        if hasattr(user, "doctor") and appointment.doctor != user.doctor:
            return Response({"error": "Not allowed to delete this appointment."}, status=status.HTTP_403_FORBIDDEN)
        if hasattr(user, "customer") and appointment.customer != user.customer:
            return Response({"error": "Not allowed to delete this appointment."}, status=status.HTTP_403_FORBIDDEN)

        appointment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)