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
            TicketMessage.objects.create(ticket=ticket, sender=request.user, message=msg)
            return redirect('ticket_detail', ticket_id=ticket_id)

    return render(request, 'support_chat.html', {
        'ticket': ticket,
        'messages': messages,
        'data': data,
        'active_id': ticket.id  # ✅ This enables active highlighting in template
    })


