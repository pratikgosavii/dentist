from django.shortcuts import render

# Create your views here.




from masters.serializers import TreatmentSerializer
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
        qs = medicine.objects.filter(is_active=True)

            # Doctor can see their own medicines + superadmin medicines
        return qs.filter(
            Q(created_by=self.request.user) | Q(created_by__is_superuser=True)
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
        try:
            doctor_instance = doctor.objects.get(user=self.request.user)
        except doctor.DoesNotExist:
            raise serializers.ValidationError("You are not registered as a doctor.")

        appointment = serializer.validated_data.get("appointment")

        if appointment.doctor != doctor_instance:
            raise serializers.ValidationError(
                "You cannot prescribe medicines for an appointment that is not booked under you."
            )

        # Patient is appointment.user
        serializer.save(
            doctor=doctor_instance,
            user=appointment.user
        )

    def get_queryset(self):
        try:
            doctor_instance = doctor.objects.get(user=self.request.user)
        except doctor.DoesNotExist:
            return Appoinment_Medicine.objects.none()

        return Appoinment_Medicine.objects.filter(doctor=doctor_instance)






class TreatmentAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, treatment_id=None):
        """
        - If `treatment_id` is provided -> return single treatment with steps
        - If not -> return all active treatments with steps
        """
        if treatment_id:
            try:
                instance = treatment.objects.get(id=treatment_id, is_active=True)
            except treatment.DoesNotExist:
                return Response({"error": "Treatment not found"}, status=status.HTTP_404_NOT_FOUND)

            serializer = TreatmentSerializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # list all active treatments
        queryset = treatment.objects.filter(is_active=True)
        serializer = TreatmentSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class AppointmentsListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, appointment_id=None):
        # make sure the logged-in user is a doctor
        try:
            doctor_instance = doctor.objects.get(user=request.user)
        except doctor.DoesNotExist:
            return Response(
                {"error": "You are not registered as a doctor."},
                status=status.HTTP_403_FORBIDDEN
            )

        if appointment_id:  # fetch single appointment
            appointment = get_object_or_404(
                Appointment,
                id=appointment_id,
                doctor=doctor_instance
            )
            serializer = AppointmentSerializer(appointment)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # fetch all appointments
        appointments = Appointment.objects.filter(
            doctor=doctor_instance
        ).order_by('-date', '-time')

        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from customer.models import Appointment
from .serializer import AppointmentTreatmentSerializer




class AppointmentTreatmentViewSet(viewsets.ModelViewSet):
    serializer_class = AppointmentTreatmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        try:
            doctor_instance = doctor.objects.get(user=self.request.user)
        except doctor.DoesNotExist:
            return AppointmentTreatment.objects.none()
        return AppointmentTreatment.objects.filter(doctor=doctor_instance)

    def perform_create(self, serializer):
        # ensure doctor owns appointment
        doctor_instance = get_object_or_404(doctor, user=self.request.user)
        appointment_id = self.kwargs.get("appointment_id")
        appointment = get_object_or_404(Appointment, id=appointment_id, doctor=doctor_instance)

        serializer.save(doctor=doctor_instance, appointment=appointment)
        


        
class AppointmentDocumentViewSet(viewsets.ModelViewSet):
    serializer_class = AppointmentDocumentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only documents of appointments this user is related to
        appointment_id = self.request.query_params.get("appointment_id")  # ?appointment_id=123
        qs = AppointmentDocument.objects.filter(uploaded_by=self.request.user)

        if appointment_id:
            qs = qs.filter(appointment_id=appointment_id)

        return qs


    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.file.delete(save=False)  # delete file from storage
        instance.delete()
        return Response({"detail": "Document deleted successfully."}, status=status.HTTP_200_OK)
    

class DoctorAppointmentViewSet(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Doctor sees only their own appointments
        qs = Appointment.objects.filter(doctor__user=self.request.user)

        # Optional filter by date (?date=YYYY-MM-DD)
        date = self.request.query_params.get("date")
        print(date)
        if date:
            qs = qs.filter(date=date)

        return qs
    
    

    def _check_doctor_permission(self, appointment, user):
        """Ensure only assigned doctor can change status."""
        if appointment.doctor.user != user:
            return False
        return True

    @action(detail=True, methods=["post"])
    def accept(self, request, pk=None):
        appointment = self.get_object()
        if not self._check_doctor_permission(appointment, request.user):
            return Response({"error": "You are not assigned to this appointment."},
                            status=status.HTTP_403_FORBIDDEN)

        appointment.status = "accepted"
        appointment.save()
        return Response({"detail": "Appointment accepted."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def reject(self, request, pk=None):
        appointment = self.get_object()
        if not self._check_doctor_permission(appointment, request.user):
            return Response({"error": "You are not assigned to this appointment."},
                            status=status.HTTP_403_FORBIDDEN)

        appointment.status = "rejected"
        appointment.save()
        return Response({"detail": "Appointment rejected."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def reschedule(self, request, pk=None):
        appointment = self.get_object()
        if not self._check_doctor_permission(appointment, request.user):
            return Response({"error": "You are not assigned to this appointment."},
                            status=status.HTTP_403_FORBIDDEN)

        new_date = request.data.get("date")
        new_time = request.data.get("time")

        if not new_date or not new_time:
            return Response({"error": "date and time are required to reschedule."},
                            status=status.HTTP_400_BAD_REQUEST)

        appointment.date = new_date
        appointment.time = new_time
        appointment.status = "waiting"  # back to waiting for confirmation
        appointment.save()
        return Response({"detail": "Appointment rescheduled."}, status=status.HTTP_200_OK)
    


    
class LabViewSet(viewsets.ModelViewSet):
    queryset = Lab.objects.all()
    serializer_class = LabSerializer
    permission_classes = [permissions.IsAuthenticated]


class LabWorkViewSet(viewsets.ModelViewSet):
    serializer_class = LabWorkSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return LabWork.objects.all().order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save()




class OfferViewSet(viewsets.ModelViewSet):
    serializer_class = OfferSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only return offers created by logged-in user
        return Offer.objects.filter(user=self.request.user).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # store logged-in user