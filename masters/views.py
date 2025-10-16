from django.shortcuts import get_object_or_404, render

# Create your views here.




from django.http import JsonResponse


from django.shortcuts import render

from customer.models import Appointment


# Create your views here.


from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from django.urls import reverse
from django.http.response import HttpResponseRedirect
from .serializers import *

from users.permissions import *

from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import medicine





@login_required(login_url='login_admin')
def add_coupon(request):

    if request.method == 'POST':

        forms = coupon_Form(request.POST, request.FILES)

        if forms.is_valid():
            forms.save()
            return redirect('list_coupon')
        else:
            print(forms.errors)
            context = {
                'form': forms
            }
            return render(request, 'add_coupon.html', context)
    
    else:

        forms = coupon_Form()

        context = {
            'form': forms
        }
        return render(request, 'add_coupon.html', context)

        

@login_required(login_url='login_admin')
def update_coupon(request, coupon_id):

    if request.method == 'POST':

        instance = coupon.objects.get(id=coupon_id)

        forms = coupon_Form(request.POST, request.FILES, instance=instance)

        if forms.is_valid():
            forms.save()
            return redirect('list_coupon')
        else:
            print(forms.errors)
    
    else:

        instance = coupon.objects.get(id=coupon_id)
        forms = coupon_Form(instance=instance)

        context = {
            'form': forms
        }
        return render(request, 'add_coupon.html', context)

        

@login_required(login_url='login_admin')
def delete_coupon(request, coupon_id):

    coupon.objects.get(id=coupon_id).delete()

    return HttpResponseRedirect(reverse('list_coupon'))


@login_required(login_url='login_admin')
def list_coupon(request):

    data = coupon.objects.all()
    context = {
        'data': data
    }
    return render(request, 'list_coupon.html', context)


from django.http import JsonResponse
from .filters import *

class get_coupon(ListAPIView):
    queryset = coupon.objects.all()
    serializer_class = coupon_serializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'  # enables filtering on all fields
    filterset_class = couponFilter  # enables filtering on all fields


@login_required(login_url='login_admin')
def add_medicine(request):

    if request.method == 'POST':

        forms = medicine_Form(request.POST, request.FILES)

        if forms.is_valid():
            form_instance = forms.save(commit=False)
            form_instance.created_by = request.user  # 👈 Set the current superuser
            form_instance.save()
            return redirect('list_medicine')
        else:
            print(forms.errors)
            context = {
                'form': forms
            }
            return render(request, 'add_medicine.html', context)
    
    else:

        forms = medicine_Form()

        context = {
            'form': forms
        }
        return render(request, 'add_medicine.html', context)

        

@login_required(login_url='login_admin')
def update_medicine(request, medicine_id):

    if request.method == 'POST':

        instance = medicine.objects.get(id=medicine_id)

        forms = medicine_Form(request.POST, request.FILES, instance=instance)

        if forms.is_valid():

            form_instance = forms.save(commit=False)
            form_instance.created_by = request.user  # 👈 Set the current superuser
        
            forms.save()
            return redirect('list_medicine')
        else:
            print(forms.errors)
    
    else:

        instance = medicine.objects.get(id=medicine_id)
        forms = medicine_Form(instance=instance)

        context = {
            'form': forms
        }
        return render(request, 'add_medicine.html', context)

        

@login_required(login_url='login_admin')
def delete_medicine(request, medicine_id):

    medicine.objects.get(id=medicine_id).delete()

    return HttpResponseRedirect(reverse('list_medicine'))


@login_required(login_url='login_admin')
def list_medicine(request):

    data = medicine.objects.all()
    context = {
        'data': data
    }
    return render(request, 'list_medicine.html', context)



class get_medicine(ListAPIView):
    queryset = medicine.objects.all()
    serializer_class = medicine_serializer
    filter_backends = [DjangoFilterBackend]
    



@login_required(login_url='login_admin')
def add_slot(request):

    if request.method == 'POST':

        forms = slot_Form(request.POST, request.FILES)

        if forms.is_valid():
            form_instance = forms.save(commit=False)
            form_instance.created_by = request.user  # 👈 Set the current superuser
            form_instance.save()
            return redirect('list_slot')
        else:
            print(forms.errors)
            context = {
                'form': forms
            }
            return render(request, 'add_slot.html', context)
    
    else:

        forms = slot_Form()

        context = {
            'form': forms
        }
        return render(request, 'add_slot.html', context)

        

@login_required(login_url='login_admin')
def update_slot(request, slot_id):

    if request.method == 'POST':

        instance = slot.objects.get(id=slot_id)

        forms = slot_Form(request.POST, request.FILES, instance=instance)

        if forms.is_valid():

            form_instance = forms.save(commit=False)
            form_instance.created_by = request.user  # 👈 Set the current superuser
        
            forms.save()
            return redirect('list_slot')
        else:
            print(forms.errors)
    
    else:

        instance = slot.objects.get(id=slot_id)
        forms = slot_Form(instance=instance)

        context = {
            'form': forms
        }
        return render(request, 'add_slot.html', context)

        

@login_required(login_url='login_admin')
def delete_slot(request, slot_id):

    slot.objects.get(id=slot_id).delete()

    return HttpResponseRedirect(reverse('list_slot'))


@login_required(login_url='login_admin')
def list_slot(request):

    data = slot.objects.all()
    context = {
        'data': data
    }
    return render(request, 'list_slot.html', context)



class get_slot(ListAPIView):
    queryset = slot.objects.all()
    serializer_class = slot_serializer
    filter_backends = [DjangoFilterBackend]
    



from rest_framework import generics


from rest_framework import viewsets, permissions
from .models import enquiry
from .serializers import EnquirySerializer

class EnquiryViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing Enquiries
    """
    queryset = enquiry.objects.all().order_by('-created_at')
    serializer_class = EnquirySerializer
    permission_classes = [permissions.IsAuthenticated]  # only logged-in users

    def perform_create(self, serializer):
        """
        Automatically set the logged-in user as the owner of the enquiry
        """
        serializer.save(user=self.request.user)


@login_required(login_url='login_admin')
def add_city(request):

    if request.method == 'POST':

        forms = city_Form(request.POST, request.FILES)

        if forms.is_valid():
            forms.save()

            return redirect('list_city')
        else:
            print(forms.errors)
            context = {
                'form': forms
            }
            return render(request, 'add_city.html', context)
    
    else:

        forms = city_Form()

        context = {
            'form': forms
        }
        return render(request, 'add_city.html', context)

        

@login_required(login_url='login_admin')
def update_city(request, city_id):

    if request.method == 'POST':

        instance = city.objects.get(id=city_id)

        forms = city_Form(request.POST, request.FILES, instance=instance)

        if forms.is_valid():

            
            forms.save()
            return redirect('list_city')
        else:
            print(forms.errors)
    
    else:

        instance = city.objects.get(id=city_id)
        forms = city_Form(instance=instance)

        context = {
            'form': forms
        }
        return render(request, 'add_city.html', context)

        

@login_required(login_url='login_admin')
def delete_city(request, city_id):

    city.objects.get(id=city_id).delete()

    return HttpResponseRedirect(reverse('list_city'))


@login_required(login_url='login_admin')
def list_city(request):

    data = city.objects.all()
    context = {
        'data': data
    }
    return render(request, 'list_city.html', context)



@login_required(login_url='login_admin')
def add_area(request):

    if request.method == 'POST':

        forms = area_Form(request.POST, request.FILES)

        if forms.is_valid():
            
            forms.save()
            return redirect('list_area')
        else:
            print(forms.errors)
            context = {
                'form': forms
            }
            return render(request, 'add_area.html', context)
    
    else:

        forms = area_Form()

        context = {
            'form': forms
        }
        return render(request, 'add_area.html', context)

        

@login_required(login_url='login_admin')
def update_area(request, area_id):

    if request.method == 'POST':

        instance = area.objects.get(id=area_id)

        forms = area_Form(request.POST, request.FILES, instance=instance)

        if forms.is_valid():

            forms.save()

            return redirect('list_area')
        else:
            print(forms.errors)
    
    else:

        instance = area.objects.get(id=area_id)
        forms = area_Form(instance=instance)

        context = {
            'form': forms
        }
        return render(request, 'add_area.html', context)

        

@login_required(login_url='login_admin')
def delete_area(request, area_id):

    area.objects.get(id=area_id).delete()

    return HttpResponseRedirect(reverse('list_area'))


@login_required(login_url='login_admin')
def list_area(request):

    data = city.objects.all()
    context = {
        'data': data
    }
    return render(request, 'list_city.html', context)



@login_required(login_url='login_admin')
def add_treatment(request):

    if request.method == 'POST':

        forms = treatment_Form(request.POST, request.FILES)

        if forms.is_valid():
            
            forms.save()
            return redirect('list_treatment')
        else:
            print(forms.errors)
            context = {
                'form': forms
            }
            return render(request, 'add_treatment.html', context)
    
    else:

        forms = treatment_Form()

        context = {
            'form': forms
        }
        return render(request, 'add_treatment.html', context)

        

@login_required(login_url='login_admin')
def update_treatment(request, treatment_id):

    if request.method == 'POST':

        instance = treatment.objects.get(id=treatment_id)

        forms = treatment_Form(request.POST, request.FILES, instance=instance)

        if forms.is_valid():

            forms.save()

            return redirect('list_treatment')
        else:
            print(forms.errors)
    
    else:

        instance = treatment.objects.get(id=treatment_id)
        forms = treatment_Form(instance=instance)

        context = {
            'form': forms
        }
        return render(request, 'add_treatment.html', context)

        

@login_required(login_url='login_admin')
def delete_treatment(request, treatment_id):

    treatment.objects.get(id=treatment_id).delete()

    return HttpResponseRedirect(reverse('list_treatment'))


@login_required(login_url='login_admin')
def list_treatment(request):

    data = treatment.objects.all()
    context = {
        'data': data
    }
    return render(request, 'list_city.html', context)



@login_required(login_url='login_admin')
def add_treatment(request):

    if request.method == 'POST':

        forms = treatment_Form(request.POST, request.FILES)

        if forms.is_valid():
            
            forms.save()
            return redirect('list_treatment')
        else:
            print(forms.errors)
            context = {
                'form': forms
            }
            return render(request, 'add_treatment.html', context)
    
    else:

        forms = treatment_Form()

        context = {
            'form': forms
        }
        return render(request, 'add_treatment.html', context)

        

@login_required(login_url='login_admin')
def update_treatment(request, treatment_id):

    if request.method == 'POST':

        instance = treatment.objects.get(id=treatment_id)

        forms = treatment_Form(request.POST, request.FILES, instance=instance)

        if forms.is_valid():

            forms.save()

            return redirect('list_treatment')
        else:
            print(forms.errors)
    
    else:

        instance = treatment.objects.get(id=treatment_id)
        forms = treatment_Form(instance=instance)

        context = {
            'form': forms
        }
        return render(request, 'add_treatment.html', context)

        

@login_required(login_url='login_admin')
def delete_treatment(request, treatment_id):

    treatment.objects.get(id=treatment_id).delete()

    return HttpResponseRedirect(reverse('list_treatment'))


@login_required(login_url='login_admin')
def list_treatment(request):

    data = treatment.objects.all()
    context = {
        'data': data
    }
    return render(request, 'list_treatment.html', context)



@login_required(login_url='login_admin')
def add_treatment_steps(request, treatment_step_id):

    treatment_instance = get_object_or_404(treatment, id=treatment_step_id)


    if request.method == 'POST':

        forms = TreatmentStepForm(request.POST, request.FILES)

        if forms.is_valid():
            step = forms.save(commit=False)
            step.treatment = treatment_instance  # auto-assign treatment
            step.save()
            forms.save()
            return redirect('treatment_step_list', treatment_id=treatment_instance.id)
        else:
            print(forms.errors)
            context = {
                'form': forms,
            'treatment': treatment_instance,

            }
            return render(request, 'add_treatment_step.html', context)
    
    else:

        forms = TreatmentStepForm()

        context = {
            'form': forms,
            'treatment': treatment_instance,
        }
        return render(request, 'add_treatment_step.html', context)

        

@login_required(login_url='login_admin')
def update_treatment_steps(request, treatment_step_id):

    if request.method == 'POST':

        instance = TreatmentStep.objects.get(id=treatment_step_id)

        forms = TreatmentStepForm(request.POST, request.FILES, instance=instance)

        if forms.is_valid():

            forms.save()

            return redirect('treatment_step_list', treatment_id=instance.treatment.id)

        else:
            print(forms.errors)
    
    else:

        instance = TreatmentStep.objects.get(id=treatment_step_id)
        forms = TreatmentStepForm(instance=instance)

        context = {
            'form': forms
        }
        return render(request, 'add_treatment_steps.html', context)

        

@login_required(login_url='login_admin')
def delete_treatment_steps(request, treatment_step_id):
    step = get_object_or_404(TreatmentStep, id=treatment_step_id)
    treatment_id = step.treatment.id   # store treatment id before delete
    step.delete()
    return redirect('treatment_step_list', treatment_id=treatment_id)



def list_treatment_steps(request, treatment_id):
    treatment_instance = get_object_or_404(treatment, id=treatment_id)
    steps = treatment_instance.steps.all()
    return render(request, "list_treatment_step.html", {"treatment": treatment_instance, "steps": steps})




@login_required(login_url='login_admin')
def update_enquiry(request, enquiry_id):

    if request.method == 'POST':

        instance = enquiry.objects.get(id=enquiry_id)

        forms = enquiry_Form(request.POST, request.FILES, instance=instance)

        if forms.is_valid():

            forms.save()

            return redirect('list_enquiry')
        else:
            print(forms.errors)
    
    else:

        instance = enquiry.objects.get(id=enquiry_id)
        forms = enquiry_Form(instance=instance)

        context = {
            'form': forms
        }
        return render(request, 'add_enquiry.html', context)

        

@login_required(login_url='login_admin')
def delete_enquiry(request, enquiry_id):

    enquiry.objects.get(id=enquiry_id).delete()

    return HttpResponseRedirect(reverse('list_enquiry'))


from .filters import EnquiryFilter, AppointmentFilter

@login_required(login_url='login_admin')
def list_enquiry(request):
    enquiry_qs = enquiry.objects.all().order_by('-created_at')
    enquiry_filter = EnquiryFilter(request.GET, queryset=enquiry_qs)
    context = {
        'filter': enquiry_filter,
        'data': enquiry_filter.qs
    }
    return render(request, 'list_enquiry.html', context)


@login_required(login_url='login_admin')
def list_apppoinments(request):
    appointment_qs = Appointment.objects.all().order_by('-date')
    appointment_filter = AppointmentFilter(request.GET, queryset=appointment_qs)
    context = {
        'filter': appointment_filter,
        'data': appointment_filter.qs
    }
    return render(request, 'list_apppoinments.html', context)




def add_home_banner(request):
    
    if request.method == "POST":

        forms = home_banner_Form(request.POST, request.FILES)

        if forms.is_valid():
            forms.save()
            return redirect('list_home_banner')
        else:
            print(forms.errors)
            context = {
                'form': forms
            }

            return render(request, 'add_home_banner.html', context)
    
    else:

        # create first row using admin then editing only

        

        return render(request, 'add_home_banner.html', { 'form' : home_banner_Form()})

def update_home_banner(request, home_banner_id):
    
    instance = home_banner.objects.get(id = home_banner_id)

    if request.method == "POST":


        instance = home_banner.objects.get(id=home_banner_id)

        forms = home_banner_Form(request.POST, request.FILES, instance=instance)

        if forms.is_valid():
            forms.save()
            return redirect('list_home_banner')
        else:
            print(forms.errors)
            context = {
                'form': forms
            }

            return render(request, 'add_home_banner.html', context)

    
    else:

        # create first row using admin then editing only

        forms = home_banner_Form(instance=instance)
                
        context = {
            'form': forms
        }

        return render(request, 'add_home_banner.html', context)


def list_home_banner(request):

    data = home_banner.objects.all()

    return render(request, 'list_home_banner.html', {'data' : data})


def delete_home_banner(request, home_banner_id):

    data = home_banner.objects.get(id = home_banner_id).delete()

    return redirect('list_home_banner')


from django.views import View

def get_home_banner(request):
  
    data = home_banner.objects.all()  # Assuming home_banner is the model name


    serialized_data = HomeBannerSerializer(data, many=True, context={'request': request}).data
    return JsonResponse({"data": serialized_data}, status=200)



def add_faq(request):
    
    if request.method == "POST":

        forms = HelpQuestion_Form(request.POST, request.FILES)

        if forms.is_valid():
            forms.save()
            return redirect('list_faq')
        else:
            print(forms.errors)
            context = {
                'form': forms
            }

            return render(request, 'add_faq.html', context)
    
    else:

        # create first row using admin then editing only

        

        return render(request, 'add_faq.html', { 'form' : HelpQuestion_Form()})

def update_faq(request, faq_id):
    
    instance = HelpQuestion.objects.get(id = faq_id)

    if request.method == "POST":


        instance = HelpQuestion.objects.get(id=faq_id)

        forms = HelpQuestion_Form(request.POST, request.FILES, instance=instance)

        if forms.is_valid():
            forms.save()
            return redirect('list_faq')
        else:
            print(forms.errors)
            context = {
                'form': forms
            }

            return render(request, 'add_faq.html', context)

    
    else:

        # create first row using admin then editing only

        forms = HelpQuestion_Form(instance=instance)
                
        context = {
            'form': forms
        }

        return render(request, 'add_faq.html', context)


def list_faq(request):

    data = HelpQuestion.objects.all()

    return render(request, 'list_faq.html', {'data' : data})


def delete_faq(request, faq_id):

    data = HelpQuestion.objects.get(id = faq_id).delete()

    return redirect('list_faq')


from django.views import View


class get_faq(ListAPIView):
    queryset = HelpQuestion.objects.all()
    serializer_class = HelpQuestionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['for_doctor'] 



def view_appointment_detail(request, appointment_id):
    
    appointment = Appointment.objects.get(id=appointment_id)
    context = {'appointment': appointment}
    return render(request, 'view_appointment.html', context)


@login_required(login_url='login_admin')
def list_support_tickets(request):
    data = SupportTicket.objects.all().order_by('-created_at')
    return render(request, 'support_chat.html', {'data': data})



@login_required(login_url='login_admin')
def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(SupportTicket, id=ticket_id)
    messages = ticket.messages.all().order_by('created_at')
    data = SupportTicket.objects.all().order_by('-created_at')

    if request.method == "POST":
        msg = request.POST.get('message')
        if msg:
            TicketMessage.objects.create(ticket=ticket, sender=request.user, is_admin = True, message=msg)
            return redirect('ticket_detail', ticket_id=ticket_id)

    return render(request, 'support_chat.html', {
        'ticket': ticket,
        'messages': messages,
        'data': data,
        'active_id': ticket.id  # ✅ This enables active highlighting in template
    })






def list_paiddoubts(request):
    """All PaidDoubt list with mobile filter"""
    paiddoubts = PaidDoubt.objects.select_related('user').order_by('-created_at')

    # Apply filter
    paiddoubt_filter = PaidDoubtFilter(request.GET, queryset=paiddoubts)
    paiddoubts = paiddoubt_filter.qs

    return render(request, "list_paiddoubt.html", {"paiddoubts": paiddoubts, "filterset": paiddoubt_filter})




def list_prescription(request):
    """All prescriptions list"""

    mobile = request.GET.get('mobile')
    print(mobile)
    user = None

    if mobile:
        user = User.objects.filter(mobile=mobile).first()
        if user:
            prescriptions = Prescription.objects.filter(user=user).order_by('-date')
        else:
            prescriptions = None
    else:
        prescriptions = Prescription.objects.select_related('user').order_by('-date')
    return render(request, "list_prescription.html", {"prescriptions": prescriptions})


def prescription_medicine_list(request, prescription_id):
    prescription = get_object_or_404(Prescription, id=prescription_id)
    medicines = prescription.medicines.select_related('medicine')
    return render(request, 'list_prescription_medicine.html', {
        'prescription': prescription,
        'medicines': medicines
    })




def create_prescription(request):
    user_id = request.GET.get('user_id')  # from search or Add New
    selected_user = None
    if user_id:
        selected_user = get_object_or_404(User, pk=user_id)

    medicines = medicine.objects.all()

    if request.method == "POST":


        print(request.POST)
        user_id_post = request.POST.get("user")
        title = request.POST.get("title")
        description = request.POST.get("description")

        if not user_id_post or not title:
            return redirect(request.path)

        user_instance = get_object_or_404(User, pk=user_id_post)

        # Create prescription
        pres = Prescription.objects.create(
            user=user_instance,
            title=title,
            description=description
        )

        # Loop through medicine fields
        med_ids = request.POST.getlist("medicine[]")
        quantities = request.POST.getlist("quantity[]")
        doses = request.POST.getlist("dose[]")
        dose_times = request.POST.getlist("dose_time[]")
        meal_relations = request.POST.getlist("meal_relation[]")
        durations = request.POST.getlist("duration_in_days[]")
        instructions_list = request.POST.getlist("instructions[]")

        for i in range(len(med_ids)):
            if med_ids[i]:
                PrescriptionMedicine.objects.create(
                    prescription=pres,
                    medicine_id=med_ids[i],
                    quantity=quantities[i] or 1,
                    dose=doses[i],
                    dose_time=dose_times[i],
                    meal_relation=meal_relations[i],
                    duration_in_days=durations[i] or 1,
                    instructions=instructions_list[i]
                )

        return redirect("list_prescription")  # replace with your list url

    return render(request, "add_prescription.html", {
        "user": selected_user,
        "medicines": medicines
    })




def update_prescription(request, pk):
    prescription = get_object_or_404(Prescription, pk=pk)
    medicines = medicine.objects.all()
    selected_user = prescription.user

    # Add choices here (for template dropdowns)
    dose_choices = PrescriptionMedicine._meta.get_field('dose').choices
    dose_time_choices = PrescriptionMedicine._meta.get_field('dose_time').choices
    meal_relation_choices = PrescriptionMedicine._meta.get_field('meal_relation').choices

    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")

        if not title:
            return redirect(request.path)

        prescription.title = title
        prescription.description = description
        prescription.save()

        # Delete existing medicines before re-adding
        prescription.medicines.all().delete()

        med_ids = request.POST.getlist("medicine[]")
        quantities = request.POST.getlist("quantity[]")
        doses = request.POST.getlist("dose[]")
        dose_times = request.POST.getlist("dose_time[]")
        meal_relations = request.POST.getlist("meal_relation[]")
        durations = request.POST.getlist("duration_in_days[]")
        instructions_list = request.POST.getlist("instructions[]")

        for i in range(len(med_ids)):
            if med_ids[i]:
                PrescriptionMedicine.objects.create(
                    prescription=prescription,
                    medicine_id=med_ids[i],
                    quantity=quantities[i] or 1,
                    dose=doses[i],
                    dose_time=dose_times[i],
                    meal_relation=meal_relations[i],
                    duration_in_days=durations[i] or 1,
                    instructions=instructions_list[i]
                )

        return redirect("list_prescription")

    prescription_medicines = prescription.medicines.select_related('medicine').all()

    return render(request, "update_prescription.html", {
        "prescription": prescription,
        "user": selected_user,
        "medicines": medicines,
        "prescription_medicines": prescription_medicines,
        "dose_choices": dose_choices,
        "dose_time_choices": dose_time_choices,
        "meal_relation_choices": meal_relation_choices,
    })




class UserPrescriptionListView(generics.ListAPIView):
    serializer_class = PrescriptionSerializer

    def get_queryset(self):
        user = self.request.user
        return Prescription.objects.filter(user = user).order_by('-created_at')