"""
Appointment status notification messages and send logic.
Creates in-app Notification records and sends push to patient/doctor.
"""
import logging
from django.utils import timezone
from .models import Notification, Appointment
from .push_services import send_push_notification

logger = logging.getLogger(__name__)


def _format_date(appointment):
    """Format appointment date for display e.g. '23 Jan 2026'."""
    if not appointment or not appointment.date:
        return ""
    return appointment.date.strftime("%d %b %Y")


def _patient_name(appointment):
    """Patient display name for doctor-facing messages."""
    if not appointment or not appointment.user:
        return "Patient"
    u = appointment.user
    name = (u.first_name or "").strip() or (u.last_name or "").strip()
    return name or "Patient"


# ---- Messages for PATIENT (customer) ----
def get_patient_message(status, appointment):
    """
    Get (title, body) for patient notification based on appointment status.
    """
    date_str = _format_date(appointment)
    messages = {
        "accepted": ("Appointment Accepted", "Your appointment has been accepted."),
        "rejected": ("Appointment Rejected", "Your appointment has been rejected by the doctor."),
        "rescheduled": ("Appointment Rescheduled", "Your appointment has been Rescheduled."),
        "next_appointment": (
            "Next Appointment Booked",
            f"Your Next appointment has been booked for {date_str}." if date_str else "Your Next appointment has been booked.",
        ),
        "rescheduled_by_patient": (
            "Appointment Rescheduled",
            "You have successfully rescheduled your appointment.",
        ),
        "completed": (
            "Appointment Completed",
            "Congratulations! Your appointment has been successfully completed.",
        ),
        "cancelled": ("Appointment Cancelled", "Your appointment has been cancelled."),
    }
    return messages.get(status, ("Appointment Update", f"Your appointment status: {status}."))


# ---- Messages for DOCTOR (dentist) ----
def get_doctor_message(status, appointment):
    """
    Get (title, body) for doctor notification based on appointment status.
    """
    date_str = _format_date(appointment)
    patient = _patient_name(appointment)
    messages = {
        "new_appointment": ("New Appointment", "You have got a new appointment."),
        "rescheduled": ("Appointment Rescheduled", "Your appointment has been Rescheduled."),
        "next_appointment": (
            "Next Appointment Booked",
            f"Your Next appointment has been booked for {date_str}." if date_str else "Your Next appointment has been booked.",
        ),
        "rescheduled_by_patient": (
            "Patient Rescheduled",
            f"{patient} has rescheduled your appointment.",
        ),
        "completed": (
            "Appointment Completed",
            f"Congratulations! Your appointment with {patient} has been successfully completed.",
        ),
        "cancelled": ("Appointment Cancelled", f"{patient} has cancelled the appointment."),
    }
    return messages.get(status, ("Appointment Update", f"Appointment status: {status}."))


def _create_and_send(user, title, body, appointment, recipient_type):
    """Create Notification record and send push to user."""
    logger.info(
        "[NOTIFICATION] Sending to %s (user_id=%s, recipient=%s) | appointment_id=%s | title=%s",
        getattr(user, "mobile", user.pk), user.pk, recipient_type,
        appointment.id if appointment else None, title,
    )
    print(f"[NOTIFICATION] Sending to user_id={user.pk} recipient={recipient_type} appointment_id={appointment.id if appointment else None} | {title}: {body}")
    Notification.objects.create(
        user=user,
        title=title,
        body=body,
        appointment=appointment,
        recipient_type=recipient_type,
    )
    # Data payload for tap-to-open: app can read appointment_id and screen to open appointment
    data = None
    if appointment:
        data = {
            "appointment_id": str(appointment.id),
            "screen": "appointment",  # so app can route to appointment screen on tap
        }
    send_push_notification(user, title, body, data=data)


def notify_appointment_status(appointment, new_status, notify_patient=True, notify_doctor=True):
    """
    Create notifications and send push for both patient and doctor based on new_status.

    Call this after updating appointment.status.

    Status values: accepted, rejected, rescheduled, next_appointment, rescheduled_by_patient, completed, cancelled.
    """
    if not appointment:
        return
    logger.info("[NOTIFICATION] notify_appointment_status appointment_id=%s new_status=%s notify_patient=%s notify_doctor=%s",
                appointment.id, new_status, notify_patient, notify_doctor)
    print(f"[NOTIFICATION] notify_appointment_status appointment_id={appointment.id} status={new_status} (patient={notify_patient}, doctor={notify_doctor})")

    if notify_patient and appointment.user:
        title, body = get_patient_message(new_status, appointment)
        _create_and_send(appointment.user, title, body, appointment, "patient")

    if notify_doctor and appointment.doctor and appointment.doctor.user:
        # For doctor, "accepted" is same as patient message context; doctor doesn't get "accepted" as status change
        # Use same status key; for "new_appointment" we call this with status="new_appointment" from create flow
        title, body = get_doctor_message(new_status, appointment)
        _create_and_send(appointment.doctor.user, title, body, appointment, "doctor")


def notify_new_appointment_to_doctor(appointment):
    """When a customer creates an appointment (waiting), notify the doctor."""
    if not appointment or not appointment.doctor:
        return
    doctor_user = getattr(appointment.doctor, "user", None)
    if not doctor_user:
        return
    logger.info("[NOTIFICATION] notify_new_appointment_to_doctor appointment_id=%s doctor_id=%s", appointment.id, doctor_user.pk)
    print(f"[NOTIFICATION] notify_new_appointment_to_doctor appointment_id={appointment.id} doctor_id={doctor_user.pk}")
    title, body = get_doctor_message("new_appointment", appointment)
    _create_and_send(doctor_user, title, body, appointment, "doctor")
