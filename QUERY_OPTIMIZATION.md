# Query Optimization Guide

This document summarizes the database indexes added across the project and provides best practices for maximizing query speed.

---

## Indexes Added

### users/models.py
- **User**: `(is_doctor, date_joined)`, `(is_customer)`, `(email)` – dashboard, user lists, duplicate checks
- **OTP**: `(mobile, is_verified)` – OTP lookups

### customer/models.py
- **Appointment**: `(user, -created_at)`, `(doctor, date)`, `(doctor, date, status)`, `(-created_at)` – appointment lists, slot checks, dashboard
- **Notification**: `(user, -created_at)` – notification list API
- **SupportTicket**: `(user, -created_at)` – support ticket list
- **PaidDoubt**: `(payment_status, -created_at)`, `(user, payment_status)` – dashboard, payment history

### doctor/models.py
- **doctor**: `(is_active)` – doctor list filter
- **DoctorAvailability**: `(doctor, day, is_active)` – weekly availability, slot filter
- **DoctorLeave**: `unique_together (doctor, leave_date)` – leave lookups
- **Appoinment_Medicine**: `(appointment, -created_at)` – medicines by appointment
- **AppointmentTreatment**: `(appointment, -created_at)` – treatments by appointment
- **LabWork**: `(appointment, -created_at)`, `(lab, status)` – lab work lists
- **AppointmentDocument**: `(appointment, -uploaded_at)` – documents by appointment
- **Expense**: `(user, date)` – expense reports
- **Offer**: `(user, -created_at)` – offer list
- **video_call_history**: `(doctor, -timestamp)`, `(user, -timestamp)` – call history

### masters/models.py
- **coupon**: `(is_active, end_date)` – valid coupons
- **medicine**: `(is_active)` – medicine list filter
- **enquiry**: `(status, -created_at)`, `(user, -created_at)` – enquiry lists
- **home_banner**: `(is_active)` – active banners
- **treatment**: `(is_active)` – treatment list filter
- **Prescription**: `(user, -created_at)` – prescription list

---

## Best Practices

### 1. Use `select_related()` for Foreign Keys

Avoid N+1 queries when accessing related objects:

```python
# Bad: N+1 queries
appointments = Appointment.objects.all()
for apt in appointments:
    print(apt.doctor.clinic_name)   # extra query per appointment

# Good: Single query with JOIN
appointments = Appointment.objects.select_related('doctor', 'user').all()
for apt in appointments:
    print(apt.doctor.clinic_name)   # no extra query
```

Use for: `Appointment`, `LabWork`, `Appoinment_Medicine`, `AppointmentTreatment`, `AppointmentDocument`, etc.

### 2. Use `prefetch_related()` for Reverse FKs and M2M

```python
# Bad: N+1
doctors = doctor.objects.filter(is_active=True)
for d in doctors:
    for slot in d.availabilities.all():  # extra query per doctor
        ...

# Good: Prefetch in 2 queries
doctors = doctor.objects.filter(is_active=True).prefetch_related('availabilities')
for d in doctors:
    for slot in d.availabilities.all():  # uses prefetched data
        ...
```

Use for: doctor availabilities, appointment medicines/treatments/documents, notifications.

### 3. Use `only()` and `defer()` for Large Models

When you need only specific fields:

```python
# Fetch only needed fields
User.objects.only('id', 'first_name', 'last_name', 'mobile')
Appointment.objects.only('id', 'date', 'status').select_related('doctor')
```

### 4. Avoid `count()` When You Don't Need It

```python
# Bad: Fetches all rows just to count
total = Appointment.objects.filter(doctor=doc).count()

# If you need both count and data, use list and len()
appointments = list(Appointment.objects.filter(doctor=doc))
total = len(appointments)
```

### 5. Use `exists()` Instead of `count() > 0`

```python
# Bad
if Appointment.objects.filter(doctor=doc, date=today).count() > 0:
    ...

# Good: Stops at first match
if Appointment.objects.filter(doctor=doc, date=today).exists():
    ...
```

### 6. Filter in Database, Not in Python

```python
# Bad: Loads all, filters in Python
all_appts = Appointment.objects.all()
my_appts = [a for a in all_appts if a.doctor_id == doc_id]

# Good: Filter in DB
my_appts = Appointment.objects.filter(doctor=doc)
```

### 7. Use `values()` / `values_list()` for Bulk Data

When you need only specific columns:

```python
# Bad: Loads full objects
ids = [a.id for a in Appointment.objects.filter(doctor=doc)]

# Good: Fetches only id
ids = list(Appointment.objects.filter(doctor=doc).values_list('id', flat=True))
```

### 8. Use `iterator()` for Large Querysets

For one-time iteration over large result sets:

```python
for apt in Appointment.objects.filter(doctor=doc).iterator(chunk_size=500):
    process(apt)
```

### 9. Common View Patterns

```python
# Appointment list for doctor dashboard
Appointment.objects.filter(doctor=doc, date__gte=start, date__lte=end)\
    .select_related('user', 'slot')\
    .order_by('-created_at')

# Customer appointment list
Appointment.objects.filter(user=user)\
    .select_related('doctor', 'slot')\
    .order_by('-created_at')

# Notification list
Notification.objects.filter(user=user)\
    .select_related('appointment')\
    .order_by('-created_at')[:20]
```

---

## Apply Migrations

After adding indexes, run:

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## Monitoring

- Use Django Debug Toolbar in development to identify N+1 queries.
- Use `django.db.connection.queries` or logging to inspect executed SQL.
- Consider `django-silk` or `django-query-profiler` for detailed profiling.
