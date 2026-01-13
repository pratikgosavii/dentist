import hmac
from django.shortcuts import get_object_or_404, render

# Create your views here.




from doctor.serializer import AppointmentDocumentSerializer, AppointmentTreatmentSerializer, doctor_serializer
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

from rest_framework import viewsets, mixins


from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, JSONParser, FormParser
from django.shortcuts import get_object_or_404
from .models import customer
from rest_framework.decorators import action

class customerViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = customer_serializer
    parser_classes = [MultiPartParser, JSONParser, FormParser]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Default retrieve/update still works with PK if needed
        return get_object_or_404(customer, user=self.request.user, is_active=True)

    @action(detail=False, methods=['get', 'put', 'patch'], url_path='me')
    def me(self, request):
        """
        Retrieve or update the logged-in customer's profile.
        """
        customer_obj = get_object_or_404(customer, user=request.user, is_active=True)

        if request.method in ['PUT', 'PATCH']:
            serializer = self.get_serializer(customer_obj, data=request.data, partial=(request.method=='PATCH'))
            serializer.is_valid(raise_exception=True)
            serializer.save()
        else:  # GET
            serializer = self.get_serializer(customer_obj)

        return Response(serializer.data)
    

    

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all().order_by('-created_at')
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["post"])
    def cancelled(self, request, pk=None):
        appointment = self.get_object()
        if appointment.user != request.user:
            return Response({"error": "This appointment does not belong to you."},
                            status=status.HTTP_403_FORBIDDEN)

        appointment.status = "cancelled"
        appointment.save()
        return Response({"detail": "Appointment cancelled."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def reschedule(self, request, pk=None):
        appointment = self.get_object()
        
        if appointment.user != request.user:
            return Response({"error": "This appointment does not belong to you."},
                            status=status.HTTP_403_FORBIDDEN)

            # ✅ Allow reschedule only if appointment is accepted
        if appointment.status.lower() != "accepted":
            return Response(
                {"error": "Only accepted appointments can be rescheduled."},
                status=status.HTTP_400_BAD_REQUEST
            )
    
        new_date = request.data.get("date")
        slot = request.data.get("slot")

        if not new_date or not slot:
            return Response({"error": "date and slot are required to reschedule."},
                            status=status.HTTP_400_BAD_REQUEST)

        appointment.date = new_date
        appointment.slot_id = slot  
        appointment.status = "rescheduled_by_patient"  
        appointment.save()

        return Response({"detail": "Appointment rescheduled successfully."},
                        status=status.HTTP_200_OK)

    def get_queryset(self):
        user = self.request.user
        qs = Appointment.objects.filter(user=user).order_by('-created_at')

        doctor_id = self.request.query_params.get('doctor_id')
        if doctor_id:
            qs = qs.filter(doctor_id=doctor_id)

        return qs



from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = doctor.objects.all().order_by("id")
    serializer_class = doctor_serializer
    permission_classes = [permissions.AllowAny]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    # ✅ Allow only GET methods
    http_method_names = ['get']


from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from doctor.models import Appoinment_Medicine
from doctor.serializer import AppointmentMedicineSerializer


class AppointmentMedicineListView(generics.ListAPIView):
    serializer_class = AppointmentMedicineSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        appointment_id = self.kwargs.get("appointment_id")

        # Ensure appointment exists and belongs to the logged-in user
        try:
            appointment = Appointment.objects.get(id=appointment_id)
        except Appointment.DoesNotExist:
            raise PermissionDenied("Appointment does not exist.")

       

        return Appoinment_Medicine.objects.filter(appointment=appointment)
    


    

class SupportTicketViewSet(viewsets.ModelViewSet):
    serializer_class = SupportTicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:  # Admin can see all tickets
            return SupportTicket.objects.all().order_by("-created_at")
        return SupportTicket.objects.filter(user=user).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    

    @action(detail=True, methods=["get", "post"], url_path="messages")
    def messages(self, request, pk=None):
        """Handle GET (list) and POST (send) messages for a ticket"""
        ticket = self.get_object()

        if request.method == "GET":
            msgs = ticket.messages.all().order_by("created_at")
            serializer = TicketMessageSerializer(msgs, many=True)
            return Response(serializer.data)

        if request.method == "POST":
            serializer = TicketMessageSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(ticket=ticket, sender=request.user)
            return Response(serializer.data, status=201)



from datetime import date, timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from doctor.models import doctor, DoctorAvailability, DoctorLeave



class DoctorWeeklyAvailabilityAPIView(APIView):
    permission_classes = [IsAuthenticated]   # if patients also call, you can remove/adjust

    def get(self, request, doctor_id, *args, **kwargs):
        doctor_instance = get_object_or_404(doctor, id=doctor_id)

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
    


    

class customer_treatment_list(viewsets.ReadOnlyModelViewSet):
    serializer_class = AppointmentTreatmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        appointment_id = self.request.query_params.get("appointment_id")

        # ✅ Only treatments for this customer's appointments
        qs = AppointmentTreatment.objects.filter(appointment__user=user)

        if appointment_id:
            qs = qs.filter(appointment_id=appointment_id)

        return qs

    def retrieve(self, request, *args, **kwargs):
        # ❌ disable detail view
        from rest_framework.response import Response
        from rest_framework import status
        return Response({"detail": "Method not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


        
class AppointmentDocumentListAPIView(ListAPIView):
    serializer_class = AppointmentDocumentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        appointment_id = self.request.query_params.get("appointment_id")
        
        qs = AppointmentDocument.objects.filter(uploaded_by=user)
        
        if appointment_id:
            qs = qs.filter(appointment_id=appointment_id)
        
        return qs
    


    

    
class ReviewViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if getattr(user, "is_customer", False):
            return Review.objects.filter(appointment__user=user)
        return Review.objects.none()  # doctors shouldn’t list reviews from here
    

    @action(detail=False, methods=["get"], url_path="doctor/(?P<doctor_id>[^/.]+)")
    def by_doctor(self, request, doctor_id=None):
        """
        Retrieve all reviews for a specific doctor by ID
        """
        from .models import Review  # lazy import if needed

        try:
            doctor_instance = doctor.objects.get(id=doctor_id)
        except doctor.DoesNotExist:
            return Response({"error": "Doctor not found"}, status=status.HTTP_404_NOT_FOUND)

        reviews = Review.objects.filter(appointment__doctor=doctor_instance)
        serializer = self.get_serializer(reviews, many=True)
        return Response(serializer.data)




class MyDoctorsAPIView(APIView):
    """
    List all doctors for which the logged-in customer has had appointments.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if not getattr(user, "is_customer", False):
            return Response({"error": "Only customers can access this."}, status=status.HTTP_403_FORBIDDEN)

        # Get all appointments for this customer
        appointments = Appointment.objects.filter(user=user).select_related('doctor')

        # Get unique doctors from these appointments
        doctor_set = {appt.doctor for appt in appointments}

        serializer = doctor_serializer(doctor_set, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    
from rest_framework.views import APIView
from rest_framework.response import Response
from .helpers import get_distance_and_eta


class NearbyDoctorsAPIView(APIView):
    def post(self, request):
        user_lat = float(request.data.get("latitude"))
        user_lon = float(request.data.get("longitude"))

        doctors = doctor.objects.filter(is_active=True)
        serializer = doctor_serializer(doctors, many=True)
        doctor_data = serializer.data

        doctors_with_distance = get_distance_and_eta(user_lat, user_lon, doctor_data)

        # ✅ Filter only within 10km (using GOOGLE distance_value)
        nearby_doctors = [
            doc for doc in doctors_with_distance if doc.get("distance_value", 0) / 1000 <= 10
        ]

        return Response({"doctors": nearby_doctors})




import razorpay
import hmac
import hashlib
from django.conf import settings
from rest_framework import viewsets
from rest_framework.decorators import action, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import PaidDoubt


razorpay_client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
)

class PaidDoubtViewSet(viewsets.ModelViewSet):
    queryset = PaidDoubt.objects.all().order_by('-id')
    serializer_class = PaidDoubtSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """
        Create PaidDoubt (Skip the Doubt) - Fixed ₹99 payment
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Save the doubt with fixed ₹99 amount
        paid_doubt = serializer.save(user=request.user, amount=99.00)

        # Create Razorpay order for ₹99
        amount_paise = 9900  # ₹99 in paise
        order_data = {
            "amount": amount_paise,
            "currency": "INR",
            "payment_capture": "1",
        }

        order = razorpay_client.order.create(order_data)

        # Save order ID in DB
        paid_doubt.razorpay_order_id = order["id"]
        paid_doubt.save()

        # Return all details to frontend for checkout
        return Response({
            "status": "success",
            "paid_doubt_id": paid_doubt.id,
            "order_id": order["id"],
            "amount": 99.00,
            "currency": "INR",
            "key": settings.RAZORPAY_KEY_ID,
        }, status=status.HTTP_201_CREATED)



# ✅ Webhook endpoint
@api_view(['POST'])
def razorpay_webhook(request):
    """
    Handle Razorpay webhook events for Skip the Doubt (₹99 payment)
    """
    webhook_secret = getattr(settings, "RAZORPAY_WEBHOOK_SECRET", None)
    received_signature = request.headers.get('X-Razorpay-Signature')

    if not webhook_secret or not received_signature:
        return Response({"error": "Missing webhook secret or signature"}, status=400)

    # Verify webhook signature
    body = request.body
    expected_signature = hmac.new(
        webhook_secret.encode('utf-8'),
        body,
        hashlib.sha256
    ).hexdigest()

    if received_signature != expected_signature:
        return Response({"error": "Invalid signature"}, status=400)

    # Parse payload
    payload = request.data
    event = payload.get('event')
    event_payload = payload.get('payload', {})
    
    # Handle payment.captured event for Skip the Doubt (₹99)
    if event == "payment.captured":
        payment_entity = event_payload.get('payment', {}).get('entity', {})
        order_id = payment_entity.get('order_id')
        payment_id = payment_entity.get('id')
        
        if order_id:
            try:
                paid_doubt = PaidDoubt.objects.get(razorpay_order_id=order_id)
                paid_doubt.payment_status = "paid"
                paid_doubt.razorpay_payment_id = payment_id
                paid_doubt.save()
            except PaidDoubt.DoesNotExist:
                pass

    return Response({"status": "ok"})
