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


from rest_framework.exceptions import ValidationError

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = doctor.objects.filter(is_active=True)
    serializer_class = doctor_serializer
    parser_classes = [MultiPartParser, JSONParser]

    def perform_create(self, serializer):
        if doctor.objects.filter(user=self.request.user).exists():
            raise ValidationError({"error": "Each user can only have one doctor profile."})
        self.instance = serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(self.get_serializer(self.instance).data, status=status.HTTP_201_CREATED)

    def perform_update(self, serializer):
        self.instance = serializer.save(user=self.request.user)

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response(self.get_serializer(self.instance).data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        doctor_obj = self.get_object()
        doctor_obj.is_active = False
        doctor_obj.save()
        return Response(
            {"message": "Doctor deactivated", "doctor": self.get_serializer(doctor_obj).data},
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["post"])
    def reactivate(self, request, pk=None):
        doc = self.get_object()
        doc.is_active = True
        doc.save()
        return Response(
            {"message": "Doctor reactivated", "doctor": self.get_serializer(doc).data},
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["get"])
    def me(self, request):
        """Get logged-in user's doctor profile"""
        try:
            doc = doctor.objects.get(user=request.user)
            return Response(self.get_serializer(doc).data, status=status.HTTP_200_OK)
        except doctor.DoesNotExist:
            return Response({"error": "Doctor profile not found"}, status=status.HTTP_404_NOT_FOUND)
        


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
    


class AppointmentMedicineViewSet(viewsets.ModelViewSet):

    queryset = Appoinment_Medicine.objects.all()
    serializer_class = AppointmentMedicineSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Appoinment_Medicine.objects.filter(user=self.request.user)
    


class TreatmentViewSet(viewsets.ModelViewSet):
    queryset = Treatment.objects.all()
    serializer_class = TreatmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Doctor sees treatments linked to their appointments
        return Treatment.objects.filter(appointment__doctor__user=self.request.user)

class TreatmentStepViewSet(viewsets.ModelViewSet):
    queryset = TreatmentStep.objects.all()
    serializer_class = TreatmentStepSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Automatically set the doctor
        serializer.save(doctor=self.request.user)

    def get_queryset(self):
        return TreatmentStep.objects.filter(treatment__appointment__doctor__user=self.request.user)
    

    from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status

class CustomerAppointmentsListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, customer_id):
        # make sure the logged-in user is a doctor
        try:
            doctor_instance = doctor.objects.get(user=request.user)
        except doctor.DoesNotExist:
            return Response(
                {"error": "You are not registered as a doctor."},
                status=status.HTTP_403_FORBIDDEN
            )

        appointments = Appointment.objects.filter(
            user_id=customer_id,
            doctor=doctor_instance
        ).order_by('-date', '-time')

        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)