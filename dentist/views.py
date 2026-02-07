
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta

from users.models import User
from doctor.models import doctor
from customer.models import Appointment, PaidDoubt


def _week_dates():
    """Return (this_week_start, last_week_start, last_week_end) for weekly comparisons."""
    now = timezone.now()
    this_week_start = now - timedelta(days=now.weekday())
    this_week_start = this_week_start.replace(hour=0, minute=0, second=0, microsecond=0)
    last_week_start = this_week_start - timedelta(days=7)
    last_week_end = this_week_start
    return this_week_start, last_week_start, last_week_end


def _growth_pct(this_val, last_val):
    """Return percentage growth; 0 if last_val is 0."""
    if last_val and last_val > 0:
        return round(((this_val - last_val) / last_val) * 100, 1)
    return 0


@login_required(login_url='login_admin')
def dashboard(request):
    this_week_start, last_week_start, last_week_end = _week_dates()

    # --- Row 1: Money ---
    subscription_revenue = User.objects.filter(is_doctor=True).aggregate(
        s=Sum('subscription_received_amount')
    )['s'] or 0
    doubt_revenue = PaidDoubt.objects.filter(payment_status='paid').aggregate(
        s=Sum('amount')
    )['s'] or 0
    total_revenue = float(subscription_revenue) + float(doubt_revenue)

    doubt_revenue_this_week = PaidDoubt.objects.filter(
        payment_status='paid', created_at__gte=this_week_start
    ).aggregate(s=Sum('amount'))['s'] or 0
    doubt_revenue_last_week = PaidDoubt.objects.filter(
        payment_status='paid',
        created_at__gte=last_week_start,
        created_at__lt=last_week_end
    ).aggregate(s=Sum('amount'))['s'] or 0
    doubt_revenue_growth = _growth_pct(float(doubt_revenue_this_week), float(doubt_revenue_last_week))

    context = {
        'total_revenue': round(total_revenue, 2),
        'subscription_revenue': round(float(subscription_revenue), 2),
        'doubt_revenue': round(float(doubt_revenue), 2),
        'doubt_revenue_growth': doubt_revenue_growth,
        'subscription_revenue_growth': 0,
        'total_revenue_growth': doubt_revenue_growth,
    }

    # --- Row 2: Counts ---
    total_appointments = Appointment.objects.count()
    appointments_this_week = Appointment.objects.filter(created_at__gte=this_week_start).count()
    appointments_last_week = Appointment.objects.filter(
        created_at__gte=last_week_start,
        created_at__lt=last_week_end
    ).count()
    context['total_appointments'] = total_appointments
    context['appointments_growth'] = _growth_pct(appointments_this_week, appointments_last_week)

    total_doubts = PaidDoubt.objects.count()
    doubts_this_week = PaidDoubt.objects.filter(created_at__gte=this_week_start).count()
    doubts_last_week = PaidDoubt.objects.filter(
        created_at__gte=last_week_start,
        created_at__lt=last_week_end
    ).count()
    context['total_doubts'] = total_doubts
    context['doubts_growth'] = _growth_pct(doubts_this_week, doubts_last_week)

    total_doctors = doctor.objects.count()
    doctors_this_week = User.objects.filter(is_doctor=True, date_joined__gte=this_week_start).count()
    doctors_last_week = User.objects.filter(
        is_doctor=True,
        date_joined__gte=last_week_start,
        date_joined__lt=last_week_end
    ).count()
    context['total_doctors'] = total_doctors
    context['doctors_growth'] = _growth_pct(doctors_this_week, doctors_last_week)

    total_users = User.objects.count()
    users_this_week = User.objects.filter(date_joined__gte=this_week_start).count()
    users_last_week = User.objects.filter(
        date_joined__gte=last_week_start,
        date_joined__lt=last_week_end
    ).count()
    context['total_users'] = total_users
    context['users_growth'] = _growth_pct(users_this_week, users_last_week)

    # --- Appointments by City (from doctor's clinic location) ---
    appointments_by_city_raw = (
        Appointment.objects
        .values('doctor__city')
        .annotate(count=Count('id'))
        .order_by('-count')
    )
    # Normalize: treat null/blank city as "Unknown"
    city_data = []
    for item in appointments_by_city_raw:
        city_name = item['doctor__city'] or 'Unknown'
        city_name = city_name.strip() or 'Unknown'
        city_data.append({'city': city_name, 'count': item['count']})
    # Compute percentages
    total_for_pct = total_appointments or 1
    for item in city_data:
        item['percent'] = round((item['count'] / total_for_pct) * 100, 1)
    context['appointments_by_city'] = city_data

    return render(request, 'adminDashboard.html', context)
