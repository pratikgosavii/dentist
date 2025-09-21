from django.db import models

# Create your models here.


from masters.models import *
from users.models import User
from .models import *

from datetime import datetime
from datetime import date
from users.models import User



def current_time():
    return datetime.now().time()


import uuid

class customer(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="customer")
    
    patient_id = models.CharField(max_length=50, unique=True, editable=False, null=True, blank=True)  # auto, read-only

    created_by = models.ForeignKey('doctor.doctor', on_delete=models.SET_NULL, null=True, blank=True, related_name='patients')

    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.patient_id:
            self.patient_id = f"PAT-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    



GENDER_CHOICES = [
    ('Male', 'Male'),
    ('Female', 'Female'),
]

APPOINTMENT_TYPE_CHOICES = [
    ('In Person', 'In Person'),
    ('Over a Call', 'Over a Call'),
]

BOOKING_FOR_CHOICES = [
    ('Book For Your Self', 'Book For Your Self'),
    ('Booking For Someone Else', 'Booking For Someone Else'),
]


from doctor.models import doctor

STATUS_CHOICES = [
    ("waiting", "Waiting for Confirmation"),
    ("accepted", "Accepted"),
    ("completed", "Completed"),
    ("rejected", "Rejected"),
    ("canceled", "Canceled"),
]

class Appointment(models.Model):

    SERVICE_CHOICES = [
            ("aligners", "Book Aligners"),
            ("skin", "Book Skin/Hydrafacial"),
    ]
    service = models.CharField(
        max_length=50,
        choices=SERVICE_CHOICES,
        default="aligners",
    )


    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="appointments")
    doctor = models.ForeignKey(doctor, on_delete=models.CASCADE, related_name="appointments_doctor")
    appointment_type = models.CharField(max_length=20, choices=APPOINTMENT_TYPE_CHOICES, default="In Person")
    booking_for = models.CharField(max_length=40, choices=BOOKING_FOR_CHOICES, default="Book For Your Self")

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="waiting"
    )
    
    # Appointment details
    date = models.DateField()
    time = models.TimeField()

    # Patient details
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    dob = models.DateField()
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)

    concern = models.TextField(blank=True, null=True)

    # Meta info
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Appointment for {self.full_name} on {self.date} at {self.time}"




class SupportTicket(models.Model):
    ROLE_CHOICES = [
        ("doctor", "Doctor"),
        ("customer", "Customer"),
        ("admin", "Admin"),
    ]
   
    STATUS_CHOICES = [
        ("open", "Open"),
        ("in_progress", "In Progress"),
        ("resolved", "Resolved"),
        ("closed", "Closed"),
    ]

    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="support_tickets")
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)  # who created ticket
    subject = models.CharField(max_length=255)
    appointment = models.ForeignKey(
        "customer.Appointment",   # replace with your actual Appointment model
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="support_tickets"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="open")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Ticket #{self.id} - {self.subject}"



class TicketMessage(models.Model):
    ticket = models.ForeignKey(SupportTicket, on_delete=models.CASCADE, related_name="messages", blank=True, null=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_support_messages")
    message = models.TextField()
    is_admin = models.BooleanField(default=False)
    attachment = models.FileField(upload_to="support/attachments/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Msg by {self.sender.username} in Ticket {self.ticket.id}"
