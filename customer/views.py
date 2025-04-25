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
        return Appointment.objects.select_related("doctor", "slot", "patient")

    # GET /api/appointments/
    def list(self, request):
        qs = self.get_queryset()
        doctor_id = request.query_params.get("doctor")
        date = request.query_params.get("date")
        if doctor_id:
            qs = qs.filter(doctor_id=doctor_id)
        if date:
            qs = qs.filter(date=date)
        serializer = AppointmentSerializer(qs, many=True)
        return Response(serializer.data)

    # GET /api/appointments/{pk}/
    def retrieve(self, request, pk=None):
        try:
            appointment = self.get_queryset().get(pk=pk)
        except Appointment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = AppointmentSerializer(appointment)
        return Response(serializer.data)

    # POST /api/appointments/
    def create(self, request):
        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(patient=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # PUT /api/appointments/{pk}/
    def update(self, request, pk=None):
        try:
            appointment = self.get_queryset().get(pk=pk)
        except Appointment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = AppointmentSerializer(appointment, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save(patient=appointment.patient)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # PATCH /api/appointments/{pk}/
    def partial_update(self, request, pk=None):
        try:
            appointment = self.get_queryset().get(pk=pk)
        except Appointment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = AppointmentSerializer(appointment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(patient=appointment.patient)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE /api/appointments/{pk}/
    def destroy(self, request, pk=None):
        try:
            appointment = self.get_queryset().get(pk=pk)
        except Appointment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        appointment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)