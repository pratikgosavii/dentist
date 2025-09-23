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

from doctor.filters import *
from users.serializer import UserProfileSerializer



from .serializer import *
from users.permissions import *
from rest_framework.decorators import action

from rest_framework import generics, permissions
from rest_framework import viewsets, status
from rest_framework.parsers import MultiPartParser, JSONParser


from rest_framework.exceptions import ValidationError

from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, JSONParser
from .models import doctor

class DoctorViewSet(mixins.RetrieveModelMixin,
                             mixins.UpdateModelMixin,
                             viewsets.GenericViewSet):
    serializer_class = doctor_serializer
    parser_classes = [MultiPartParser, JSONParser]
    permission_classes = [IsAuthenticated]


    def get_object(self):
        return doctor.objects.get(user=self.request.user, is_active=True)

    
    
    
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
        ).order_by('-date')

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
    


from rest_framework.decorators import action



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
        slot = request.data.get("slot")

        if not new_date or not slot:
            return Response({"error": "date and time are required to reschedule."},
                            status=status.HTTP_400_BAD_REQUEST)

        appointment.date = new_date
        appointment.slot = slot
        appointment.status = "waiting"  # back to waiting for confirmation
        appointment.save()
        return Response({"detail": "Appointment rescheduled."}, status=status.HTTP_200_OK)
    

    @action(detail=False, methods=['get'], url_path='patients')
    def list_patients(self, request):
        users = User.objects.filter(
            appointments__doctor__user=request.user
        ).distinct()
        data = UserProfileSerializer(users, many=True).data
        return Response(data)
    
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


        
class InventoryProductViewSet(viewsets.ModelViewSet):
    queryset = InventoryProduct.objects.all().order_by("expiry_date")
    serializer_class = InventoryProductSerializer
    permission_classes = [permissions.IsAuthenticated]  # only logged-in users

    # You can override create/update if you want custom logic later

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from firebase_admin import auth as firebase_auth

from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

class DoctorVerifyCustomerOTP(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print(request.user)
        if not request.user.is_doctor:
            return Response({"error": "Only doctors can verify customers."}, status=403)

        id_token = request.data.get("idToken")
        if not id_token:
            return Response({"error": "idToken is required."}, status=400)

        # Optional fields
        first_name = request.data.get("first_name", "")
        last_name = request.data.get("last_name", "")
        dob = request.data.get("dob")           # "YYYY-MM-DD" string
        gender = request.data.get("gender")     # 'male' or 'female'

        try:
            decoded_token = firebase_auth.verify_id_token(id_token)
            mobile = decoded_token.get("phone_number")
            uid = decoded_token.get("uid")

            if User.objects.filter(mobile=mobile).exists():
                return Response({"error": "User already exists."}, status=400)

            # 1️⃣ Create User
            user = User.objects.create(
                mobile=mobile,
                firebase_uid=uid,
                is_customer=True,
                first_name=first_name,
                last_name=last_name,
                dob=dob,
                gender=gender
            )

            # 2️⃣ Create Customer profile and link to doctor
            cust = customer.objects.create(
                user=user,
                created_by=request.user.doctor
            )

            # 3️⃣ Generate JWT tokens
            refresh = RefreshToken.for_user(user)

            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": {
                    "id": user.id,
                    "mobile": user.mobile,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "dob": user.dob,
                    "gender": user.gender,
                    "customer_id": cust.id,
                    "created_by_doctor": request.user.doctor.id
                }
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)




class AppointmentLedgerViewSet(viewsets.ModelViewSet):
    serializer_class = AppointmentLedgerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # show ledgers only for appointments belonging to this doctor
        user = self.request.user
        if hasattr(user, "is_doctor"):

            # if appointment id is passed, filter further
            appointment_id = self.request.query_params.get("appointment_id")
            print()
            if appointment_id:
                return AppointmentLedger.objects.filter(appointment_id=appointment_id, appointment__doctor=user.doctor)


    def perform_create(self, serializer):
        # ensure ledger belongs to a doctor’s appointment
        appointment = serializer.validated_data["appointment"]
        if appointment.doctor != self.request.user.doctor:
            return Response({"error": "ou cannot add a ledger to this appointment."},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer.save()




from django.db.models import Sum

class DoctorEarningAPIView(APIView):
    """
    API view to return earnings report for the logged-in doctor.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            doctor_instance = doctor.objects.get(user=request.user)
        except doctor.DoesNotExist:
            return Response({"detail": "Doctor profile not found."}, status=404)

        appointments = Appointment.objects.filter(doctor=doctor_instance).prefetch_related(
            'treatments__steps', 'ledgers'
        )

        report = []
        for appt in appointments:
            total_price = sum(
                step.price for treatment in appt.treatments.all() for step in treatment.steps.all()
            )
            received_amount = appt.ledgers.aggregate(total=Sum('amount'))['total'] or 0
            pending_amount = total_price - received_amount

            report.append({
                "appointment_id": appt.id,
                "patient": f"{getattr(appt.user, 'first_name', '')} {getattr(appt.user, 'last_name', '')}".strip(),
                "doctor": doctor_instance.user.get_full_name(),
                "date": appt.created_at,
                "total_price": total_price,
                "received_amount": received_amount,
                "pending_amount": pending_amount
            })

        return Response(report)



   
class list_patient(generics.ListAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # fetch distinct users who have appointments with this doctor
        return User.objects.filter(
            appointments__doctor__user=self.request.user
        ).distinct()
    


    
class DoctorLeaveViewSet(viewsets.ModelViewSet):
    serializer_class = DoctorLeaveSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        try:
            doctor_instance = doctor.objects.get(user=self.request.user)
        except doctor.DoesNotExist:
            raise serializers.ValidationError("You are not registered as a doctor.")
        # Only get leaves for logged-in doctor
        return DoctorLeave.objects.filter(doctor=doctor_instance)

    def perform_create(self, serializer):
        try:
            doctor_instance = doctor.objects.get(user=self.request.user)
        except doctor.DoesNotExist:
            raise serializers.ValidationError("You are not registered as a doctor.")
        serializer.save(doctor=doctor_instance)

   


   
class DoctorAvailabilityView(APIView):
    def post(self, request):
        serializer = DoctorAvailabilityBulkSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Availability updated successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        try:
            doctor_instance = doctor.objects.get(user=self.request.user)
        except doctor.DoesNotExist:
            raise serializers.ValidationError("You are not registered as a doctor.")
        
        slots = DoctorAvailability.objects.filter(doctor = doctor_instance)
        serializer = DoctorAvailabilitySerializer(slots, many=True)
        return Response(serializer.data)