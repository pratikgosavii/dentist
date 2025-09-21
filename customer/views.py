from django.shortcuts import get_object_or_404, render

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

from rest_framework import viewsets, mixins


from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, JSONParser
from django.shortcuts import get_object_or_404
from .models import customer
from rest_framework.decorators import action

class customerViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = customer_serializer
    parser_classes = [MultiPartParser, JSONParser]
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



class DoctorViewSet(viewsets.ReadOnlyModelViewSet):  
    queryset = doctor.objects.all().order_by("id")
    serializer_class = doctor_serializer
    permission_classes = [permissions.AllowAny]


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

        if appointment.user != self.request.user:
            raise PermissionDenied("You are not allowed to view medicines for this appointment.")

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
