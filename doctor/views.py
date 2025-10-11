from django.shortcuts import render

# Create your views here.




from customer.serializer import AppointmentSerializer
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
from rest_framework.parsers import MultiPartParser, JSONParser, FormParser
from .models import doctor

class DoctorViewSet(mixins.RetrieveModelMixin,
                             mixins.UpdateModelMixin,
                             viewsets.GenericViewSet):
    serializer_class = doctor_serializer
    parser_classes = [MultiPartParser, JSONParser, FormParser]
    permission_classes = [IsAuthenticated, IsDoctor]


    def get_object(self):
        return doctor.objects.get(user=self.request.user, is_active=True)

     # 👇 handle PATCH (partial update)
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    
    
from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend


from django.db.models import Q

class DoctorMedicineViewSet(viewsets.ModelViewSet):
    serializer_class = medicine_serializer
    permission_classes = [IsAuthenticated, IsDoctor]

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
    permission_classes = [IsAuthenticated, IsDoctor]

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

        # if accessing a single object (detail view)
        if self.action in ["retrieve", "update", "partial_update", "destroy"]:
            return Appoinment_Medicine.objects.filter(doctor=doctor_instance)

        # if listing, require appointment_id
        appointment_id = self.request.query_params.get("appointment_id")
        if appointment_id:
            return Appoinment_Medicine.objects.filter(
                appointment_id=appointment_id,
                doctor=doctor_instance
            )

        raise serializers.ValidationError("Need to pass appointment_id parameter for list view")



class TreatmentAPIView(APIView):
    permission_classes = [IsAuthenticated, IsDoctor]

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
    permission_classes = [IsAuthenticated, IsDoctor]

    def get(self, request, appointment_id=None):
        # Ensure logged-in user is a doctor
        try:
            doctor_instance = doctor.objects.get(user=request.user)
        except doctor.DoesNotExist:
            return Response(
                {"error": "You are not registered as a doctor."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Fetch single appointment by ID
        if appointment_id:
            appointment = get_object_or_404(
                Appointment,
                id=appointment_id,
                doctor=doctor_instance
            )
            serializer = AppointmentSerializer(appointment)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # Fetch all appointments or filter by date
        date_param = request.query_params.get('date')  # e.g., ?date=2025-09-24
        appointments = Appointment.objects.filter(doctor=doctor_instance)

        if date_param:
            try:
                filter_date = datetime.strptime(date_param, "%Y-%m-%d").date()
                appointments = appointments.filter(date=filter_date)
            except ValueError:
                return Response({"error": "Invalid date format. Use YYYY-MM-DD."},
                                status=status.HTTP_400_BAD_REQUEST)

        appointments = appointments.order_by('-date')
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
    permission_classes = [IsAuthenticated, IsDoctor]

    def get_queryset(self):
        """
        Return treatments for the logged-in doctor,
        optionally filtered by ?appointment_id=.
        """
        doctor_instance = doctor.objects.filter(user=self.request.user).first()
        if not doctor_instance:
            return AppointmentTreatment.objects.none()

        qs = AppointmentTreatment.objects.filter(doctor=doctor_instance)

        appointment_id = self.request.query_params.get("appointment_id")
        if appointment_id:
            qs = qs.filter(appointment_id=appointment_id)

        return qs

    def perform_create(self, serializer):
        """
        Create a treatment for the given appointment_id (passed in query params).
        """
        doctor_instance = get_object_or_404(doctor, user=self.request.user)

        appointment_id = self.request.query_params.get("appointment_id")
        if not appointment_id:
            raise ValidationError({"appointment_id": "This query param is required."})

        appointment = get_object_or_404(Appointment, id=appointment_id, doctor=doctor_instance)

        serializer.save(doctor=doctor_instance, appointment=appointment)

    def perform_update(self, serializer):
        """
        Update a treatment, ensuring appointment_id in params still matches.
        """
        doctor_instance = get_object_or_404(doctor, user=self.request.user)

        appointment_id = self.request.query_params.get("appointment_id")
        if not appointment_id:
            raise ValidationError({"appointment_id": "This query param is required."})

        appointment = get_object_or_404(Appointment, id=appointment_id, doctor=doctor_instance)

        serializer.save(doctor=doctor_instance, appointment=appointment)




        
class AppointmentDocumentViewSet(viewsets.ModelViewSet):
    serializer_class = AppointmentDocumentSerializer
    permission_classes = [IsAuthenticated, IsDoctor]

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
    serializer_class = DoctorAppointmentSerializer
    permission_classes = [IsAuthenticated, IsDoctor]


    def perform_create(self, serializer):
        """
        Doctor is always taken from request.user (must be a doctor).
        User (patient) is passed in request body as 'user'.
        """
        # ✅ fetch doctor from logged-in user
        try:
            doctor_instance = self.request.user.doctor
        except doctor.DoesNotExist:
            return Response(
                {"error": "Only doctors can create appointments."},
                status=status.HTTP_403_FORBIDDEN
            )

        # ✅ fetch patient user
        user_id = self.request.data.get("user")
        if not user_id:
            return Response(
                {"error": "User (patient) is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        patient_user = get_object_or_404(User, id=user_id)

        # ✅ save appointment with doctor + patient
        serializer.save(user=patient_user, doctor=doctor_instance)
    
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
    def completed(self, request, pk=None):
        appointment = self.get_object()
        if not self._check_doctor_permission(appointment, request.user):
            return Response({"error": "You are not assigned to this appointment."},
                            status=status.HTTP_403_FORBIDDEN)

        appointment.status = "completed"
        appointment.save()
        return Response({"detail": "Appointment marked as completed."}, status=status.HTTP_200_OK)

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
        appointment.slot__id = slot
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
    serializer_class = LabSerializer
    permission_classes = [IsAuthenticated, IsDoctor]

    def get_queryset(self):
        # Show only labs created by this doctor
        return Lab.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Automatically assign the logged-in doctor as owner
        serializer.save(user=self.request.user)



class LabWorkViewSet(viewsets.ModelViewSet):
    serializer_class = LabWorkSerializer
    permission_classes = [IsAuthenticated, IsDoctor]

    def get_queryset(self):

        appointment_id = self.request.query_params.get("appointment_id")
        if appointment_id:
            return LabWork.objects.filter(appointment__id = appointment_id).order_by("-created_at")
        return LabWork.objects.all().order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save()




class OfferViewSet(viewsets.ModelViewSet):
    serializer_class = OfferSerializer
    permission_classes = [IsAuthenticated, IsDoctor]

    def get_queryset(self):
        # Only return offers created by logged-in user
        return Offer.objects.filter(user=self.request.user).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # store logged-in user


        
class InventoryProductViewSet(viewsets.ModelViewSet):
    queryset = InventoryProduct.objects.all().order_by("expiry_date")
    serializer_class = InventoryProductSerializer
    permission_classes = [IsAuthenticated, IsDoctor]

    # You can override create/update if you want custom logic later

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from firebase_admin import auth as firebase_auth

from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

class DoctorVerifyCustomerOTP(APIView):
    permission_classes = [IsAuthenticated, IsDoctor]

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

    def get(self, request, pk=None):
        """Return one or all customers created by this doctor"""
        if not request.user.is_doctor:
            return Response({"error": "Only doctors can view their customers."}, status=403)

        if pk:  # ✅ Detail view
            cust = get_object_or_404(customer, pk=pk)
            serializer = customer_serializer(cust)
            return Response(serializer.data)

        # ✅ List view
        customers = customer.objects.all()
        serializer = customer_serializer(customers, many=True)
        return Response(serializer.data, status=200)
    


class AppointmentLedgerViewSet(viewsets.ModelViewSet):
    serializer_class = AppointmentLedgerSerializer
    permission_classes = [IsAuthenticated, IsDoctor]

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


class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated, IsDoctor]

    def get_queryset(self):
        # show ledgers only for expenses belonging to this doctor
        user = self.request.user
        if hasattr(user, "is_doctor"):

            # if expense id is passed, filter further
           
            return Expense.objects.filter(user=user)
        else:

            return Response({"error": "You are not a doctor."},
                            status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        # ensure ledger belongs to a doctor’s appointment
        serializer.save(user=self.request.user)




from django.db.models import Sum

class DoctorReportAPIView(APIView):
    """
    API view to return earnings report for the logged-in doctor.
    """
    permission_classes = [IsAuthenticated, IsDoctor]

    def get(self, request, *args, **kwargs):
        try:
            doctor_instance = doctor.objects.get(user=request.user)
        except doctor.DoesNotExist:
            return Response({"detail": "Doctor profile not found."}, status=404)

        # Appointments
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

        # Expenses
        expenses = Expense.objects.filter(user=request.user).values("id", "title", "amount", "date")

        return Response({
            "appointments": report,
            "expenses": list(expenses)   # serialize queryset to list of dicts
        })


   
class list_patient(generics.ListAPIView):
    serializer_class = customer_serializer
    permission_classes = [IsAuthenticated, IsDoctor]

    def get_queryset(self):
        # fetch distinct users who have appointments with this doctor
        return customer.objects.filter(
            user__appointments__doctor__user=self.request.user
        ).distinct()
    


    
class DoctorLeaveViewSet(viewsets.ModelViewSet):
    serializer_class = DoctorLeaveSerializer
    permission_classes = [IsAuthenticated, IsDoctor]

    from datetime import date

class DoctorLeaveViewSet(viewsets.ModelViewSet):
    serializer_class = DoctorLeaveSerializer
    permission_classes = [IsAuthenticated, IsDoctor]

    def get_queryset(self):
        try:
            doctor_instance = doctor.objects.get(user=self.request.user)
        except doctor.DoesNotExist:
            return DoctorLeave.objects.none()
        # Only future or today leaves for internal queryset
        return DoctorLeave.objects.filter(doctor=doctor_instance, leave_date__gte=date.today())

    def list(self, request, *args, **kwargs):
        try:
            doctor_instance = doctor.objects.get(user=request.user)
        except doctor.DoesNotExist:
            return Response({"error": "You are not registered as a doctor."}, status=400)

        # Only today and future leaves
        leave_dates = list(
            DoctorLeave.objects.filter(doctor=doctor_instance, leave_date__gte=date.today())
            .values_list('leave_date', flat=True)
        )
        print(date.today())
        # Only today and future appointments
        appointment_dates = list(
            Appointment.objects.filter(
                doctor=doctor_instance,
                date__gte=date.today()
            )
            .values_list('date', flat=True)
            .distinct()
        )

        return Response({
            "leave_dates": leave_dates,
            "appointment_dates": appointment_dates
        })
    


    def perform_create(self, serializer):
        try:
            doctor_instance = doctor.objects.get(user=self.request.user)
        except doctor.DoesNotExist:
            raise serializers.ValidationError("You are not registered as a doctor.")
        serializer.save(doctor=doctor_instance)

   


   
class DoctorAvailabilityView(APIView):

    permission_classes = [IsAuthenticated, IsDoctor]

    def post(self, request):
        serializer = DoctorAvailabilityBulkSerializer( data=request.data, context={"request": request}  )
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
    


    


from datetime import date, timedelta
    
class DoctorWeeklyAvailabilityAPIView(APIView):
    permission_classes = [IsAuthenticated]   # if patients also call, you can remove/adjust

    def get(self, request, *args, **kwargs):
        doctor_instance = get_object_or_404(doctor, user=request.user)

        today = date.today()
        next_7_days = [today + timedelta(days=i) for i in range(7)]

        leave_dates = set(
            DoctorLeave.objects.filter(
                doctor=doctor_instance,
                leave_date__in=next_7_days
            ).values_list("leave_date", flat=True)
        )

        availability_response = []

        for d in next_7_days:
            if d in leave_dates:
                continue

            weekday = d.strftime("%A")

            # get active availability for that doctor and weekday
            availabilities = DoctorAvailability.objects.filter(
                doctor=doctor_instance,
                day=weekday,
                is_active=True
            ).select_related("slot")

            # use your SlotSerializer
            slots = [availability.slot for availability in availabilities]
            serialized_slots = slot_serializer(slots, many=True).data

            availability_response.append({
                "date": d,
                "slots": serialized_slots
            })

        return Response(availability_response)
    


    
class ToothViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = ToothSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        # Doctors must provide a user_id to work with customer's teeth
        user_id = self.request.query_params.get("user_id")
        if user.is_doctor and user_id:
            return Tooth.objects.filter(user_id=user_id, user__is_customer=True)

        # Customers can only see their own teeth
        if user.is_customer:
            return Tooth.objects.filter(user=user)

        return Tooth.objects.none()






class MyReviewsAPIView(APIView):
    """
    Retrieve all reviews for appointments of the logged-in doctor.
    """
    permission_classes = [IsAuthenticated, IsDoctor]


    def get(self, request):
        user = request.user

        if not getattr(user, "is_doctor", False):
            return Response({"error": "Only doctors can access this."}, status=status.HTTP_403_FORBIDDEN)

        # Get all reviews where appointment.doctor.user == logged-in user
        reviews = Review.objects.filter(appointment__doctor__user=user)

        data = [
            {
                "id": r.id,
                "appointment_id": r.appointment.id,
                "user_id": r.appointment.user.id,
                "rating": r.rating,
                "comment": r.comment,
                "created_at": r.created_at
            }
            for r in reviews
        ]

        return Response(data)
    



from decimal import Decimal

import base64
from io import BytesIO
from django.template.loader import render_to_string
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from decimal import Decimal


import base64
import requests
from decimal import Decimal
from django.conf import settings
from django.template.loader import render_to_string
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class InvoicePDFAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, appointment_id):
        appointment = Appointment.objects.get(id=appointment_id)
        treatments = appointment.treatments.prefetch_related("steps")

        subtotal = Decimal(0)
        for t in treatments:
            for step in t.steps.all():
                subtotal += step.price

       
        grand_total = subtotal

        doctor_instance = appointment.doctor

        context = {
            "invoice_number": f"INV-{appointment.id}",
            "issue_date": appointment.created_at.date(),
            "doctor_name": doctor_instance.user.first_name + doctor_instance.user.last_name,
            "doctor_email": doctor_instance.user.email,
            "doctor_mobile": doctor_instance.user.mobile,
            "clinic_name": doctor_instance.clinic_name,
            "clinic_address": doctor_instance.locality + doctor_instance.house_building + doctor_instance.state + doctor_instance.city + doctor_instance.pincode,
            "treatments": treatments,
            "subtotal": subtotal,
            "grand_total": grand_total,
            "appointment": appointment,
        }

        # Render HTML template
        html_content = render_to_string("invoice.html", context)

        # Generate PDF via HTML2PDF API
        response = requests.post(
            "https://api.html2pdf.app/v1/generate",
            json={
                "html": html_content,
                "apiKey": settings.HTML2PDF_API_KEY,
                "options": {
                    "printBackground": True,
                    "margin": "1cm",
                    "pageSize": "A4",
                },
            },
        )

        if response.status_code != 200:
            return Response(
                {"error": f"PDF generation failed: {response.text}"},
                status=400,
            )

        pdf_bytes = response.content
        pdf_base64 = base64.b64encode(pdf_bytes).decode("utf-8")

        return Response({
            "message": "Invoice PDF generated successfully",
            "filename": f"invoice_{appointment.id}.pdf",
            "filetype": "application/pdf",
            "data": pdf_base64,
        })



    
class PrescriptionPDFAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, appointment_id):
        appointment = Appointment.objects.get(id=appointment_id)

        # Fetch prescribed medicines (adjust field name if needed)
        medicines = appointment.dosdsctor_medicines.select_related("medicine")

        doctor_instance = appointment.doctor

        context = {
            "appointment": appointment,
            "doctor_name": doctor_instance.user.first_name + doctor_instance.user.last_name,
            "doctor_email": doctor_instance.user.email,
            "doctor_mobile": doctor_instance.user.mobile,
            "clinic_name": doctor_instance.clinic_name,
            "clinic_address": doctor_instance.locality + doctor_instance.house_building + doctor_instance.state + doctor_instance.city + doctor_instance.pincode,
            "invoice_number": f"RX-{appointment.id}",
            "issue_date": appointment.created_at.date(),
            "medicines": medicines,
        }

        # Render HTML for prescription
        html_content = render_to_string("prescription_invoice.html", context)

        # Generate PDF using HTML2PDF API
        response = requests.post(
            "https://api.html2pdf.app/v1/generate",
            json={
                "html": html_content,
                "apiKey": settings.HTML2PDF_API_KEY,
                "options": {
                    "printBackground": True,
                    "margin": "1cm",
                    "pageSize": "A4",
                },
            },
        )

        if response.status_code != 200:
            return Response(
                {"error": f"PDF generation failed: {response.text}"},
                status=400
            )

        pdf_bytes = response.content
        pdf_base64 = base64.b64encode(pdf_bytes).decode("utf-8")

        return Response({
            "message": "Prescription PDF generated successfully",
            "filename": f"prescription_{appointment.id}.pdf",
            "filetype": "application/pdf",
            "data": pdf_base64,
        })
    



