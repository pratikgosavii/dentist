from django.db import models

# Create your models here.


from masters.models import *
from users.models import User

from .models import *

from datetime import datetime

def current_time():
    return datetime.now().time()

GENDER_CHOICES = (
    ("Male", "Male"),
    ("Female", "Female"),
    ("Other", "Other"),
)

class doctor(models.Model):

    user = models.OneToOneField('users.User', on_delete=models.CASCADE, related_name="doctor")

    # Basic Info
    image = models.ImageField(upload_to="doctor_images/", blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[
        ("Male", "Male"), ("Female", "Female"), ("Other", "Other")
    ], blank=True, null=True)

    clinic_image = models.ImageField(upload_to="clinics", blank=True, null=True)
    clinic_logo = models.ImageField(upload_to="clinic_logo", blank=True, null=True)
    
    clinic_name = models.CharField(max_length=150, blank=True, null=True)
    clinic_consultation_fees = models.IntegerField(blank=True, null=True)
    clinic_phone_number = models.CharField(max_length=15, blank=True, null=True)

    # Address
    house_building = models.CharField(max_length=120, blank=True, null=True)
    locality = models.CharField(max_length=120, blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)
    state = models.CharField(max_length=120, blank=True, null=True)
    city = models.CharField(max_length=120, blank=True, null=True)
    country = models.CharField(max_length=120, blank=True, null=True)

    # Professional Info
    designation = models.CharField(max_length=200, blank=True, null=True)   # Dentist, Orthodontist, etc.
    title = models.CharField(max_length=120, blank=True, null=True)         # Dr., Prof., etc.
    degree = models.CharField(max_length=120, blank=True, null=True)        # MDS, BDS, etc.
    specializations = models.TextField(blank=True, null=True)               # Store as comma-separated or JSON
    education = models.TextField(blank=True, null=True)                     # Education history
    about_doctor = models.TextField(blank=True, null=True)

    # Experience & Ratings
    experience_years = models.PositiveIntegerField(blank=True, null=True)   # 25+ years
    rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    review_count = models.PositiveIntegerField(default=0)

    remark = models.CharField(max_length=120, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    
    
    
    
DAYS_OF_WEEK = (
    ("Mon", "Monday"),
    ("Tue", "Tuesday"),
    ("Wed", "Wednesday"),
    ("Thu", "Thursday"),
    ("Fri", "Friday"),
    ("Sat", "Saturday"),
    ("Sun", "Sunday"),
)

# Clinic model
class Clinic(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.CharField(max_length=10)
    consultation_fee = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name


# Availability model




class video_call_history(models.Model):
    doctor = models.ForeignKey('doctor', on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)




class Appoinment_Medicine(models.Model):

    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='doctor_wdefredsasmedicines')
    medicine = models.ForeignKey('masters.medicine', on_delete=models.CASCADE, related_name='swweeq')
    doctor = models.ForeignKey('doctor', on_delete=models.CASCADE, related_name='doctor_medicines')
    appointment = models.ForeignKey('customer.Appointment', on_delete=models.CASCADE, related_name='dosdsctor_medicines')

    quantity = models.DecimalField(max_digits=4, decimal_places=1)  # Add max_digits also
    
    dose_time = models.CharField(
        max_length=20,
        choices=[
            ('morning', 'Morning'),
            ('afternoon', 'Afternoon'),
            ('night', 'Night'),
        ]
    )

    dose = models.CharField(
        max_length=20,
        choices=[
            ('half', 'Half'),
            ('1', '1'),
            ('5 ml', '5 ml'),
            ('10 ml', '10 ml'),
            ('15 ml', '15 ml'),
            ('20 ml', '20 ml'),
        ]
    )

    meal_relation = models.CharField(
        max_length=30,
        choices=[
            ('before_breakfast', 'Before Breakfast'),
            ('after_breakfast', 'After Breakfast'),
            ('before_lunch', 'Before Lunch'),
            ('after_lunch', 'After Lunch'),
            ('before_dinner', 'Before Dinner'),
            ('after_dinner', 'After Dinner'),
        ]
    )

    duration_in_days = models.PositiveIntegerField(default=1)
    instructions = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.medicine.name} "
    


class AppointmentTreatment(models.Model):
    appointment = models.ForeignKey("customer.Appointment", on_delete=models.CASCADE, related_name="treatments")
    doctor = models.ForeignKey("doctor", on_delete=models.CASCADE, related_name="appointment_treatments")
    treatment = models.ForeignKey("masters.treatment", on_delete=models.CASCADE, related_name="appointment_treatments")
    created_at = models.DateTimeField(auto_now_add=True)

class AppointmentTreatmentStep(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("active", "Active"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    appointment_treatment = models.ForeignKey(
        AppointmentTreatment,
        on_delete=models.CASCADE,
        related_name="steps"
    )
    step_number = models.PositiveIntegerField()
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00
    )
    date = models.DateField(auto_now_add=True)  # default today if not provided


    def __str__(self):
        return f"Step {self.step_number} - {self.title} ({self.status})"



class AppointmentLedger(models.Model):
    appointment = models.ForeignKey(
        "customer.Appointment", on_delete=models.CASCADE, related_name="ledgers"
    )
    title = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)  # default today if not provided

    def __str__(self):
        return f"{self.title} - {self.amount} ({self.date})"


class Expense(models.Model):
    
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)  # default today if not provided

    def __str__(self):
        return f"{self.title} - {self.amount} ({self.date})"



class AppointmentDocument(models.Model):
    appointment = models.ForeignKey(
        "customer.appointment", 
        on_delete=models.CASCADE, 
        related_name="documents"
    )
    uploaded_by = models.ForeignKey(
        User, 
        on_delete=models.CASCADE
    )
    file = models.FileField(upload_to="appointment_documents/")
    title = models.CharField(max_length=255, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title or self.file.name} - {self.appointment.id}"
    

    
class Lab(models.Model):
    name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
   

    def __str__(self):
        return self.name


class LabWork(models.Model):
    STATUS_CHOICES = [
        ("impression", "Impression"),
        ("trial", "Trial"),
        ("delivered", "Delivered"),
    ]

    lab = models.ForeignKey(Lab, on_delete=models.CASCADE, related_name="lab_works")
    appointment = models.ForeignKey("customer.Appointment", on_delete=models.CASCADE, related_name="lab_works", null = True, blank = True)
    
    type_of_work = models.CharField(max_length=150)
    tooth_number = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="impression")
    note = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Lab Work for Appointment {self.appointment.id} - {self.type_of_work}"
    



    
class Offer(models.Model):
    DISCOUNT_TYPE_CHOICES = [
        ("percentage", "Percentage"),
        ("flat", "Flat"),
    ]

    ELIGIBILITY_CHOICES = [
        ("existing", "For Existing Patients"),
        ("new", "For New Patients"),
        ("everyone", "For Everyone"),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="offers")  
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPE_CHOICES)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    valid_from = models.DateField()
    valid_to = models.DateField()
    applicable_treatments = models.CharField(max_length=255, blank=True, null=True)  # or FK/M2M if you have Treatment model
    eligibility = models.CharField(max_length=20, choices=ELIGIBILITY_CHOICES, default="everyone")
    banner = models.ImageField(upload_to="offers/banners/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title




        
class InventoryProduct(models.Model):
    name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=0)
    expiry_date = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.quantity})"
    


class DoctorAvailability(models.Model):
    doctor = models.ForeignKey('doctor', on_delete=models.CASCADE, related_name='availabilities')
    
    DAY_CHOICES = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]
    
    day = models.CharField(max_length=10, choices=DAY_CHOICES)
    slot = models.ForeignKey("masters.slot", on_delete=models.CASCADE, related_name='doctor_slots')
    
    is_active = models.BooleanField(default=True)  # in case you want to turn off that slot
    
    
    

class DoctorLeave(models.Model):
    doctor = models.ForeignKey("doctor", on_delete=models.CASCADE)  # assuming doctor is a User
    leave_date = models.DateField()

    class Meta:
        unique_together = ('doctor', 'leave_date')  # prevent duplicate leaves

   
    
    
class Tooth(models.Model):
    STATUS_CHOICES = [
        ("healthy", "Healthy"),
        ("decayed", "Decayed"),
        ("filled", "Filled"),
        ("missing", "Missing"),
        ("extracted", "Extracted"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="teeth")
    number = models.CharField(max_length=3)  # "11", "12", ..., "48"
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="healthy")

    class Meta:
        unique_together = ("user", "number")

    def __str__(self):
        return f"{self.user.username} - Tooth {self.number} : {self.status}"