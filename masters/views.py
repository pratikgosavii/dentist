from django.shortcuts import render

# Create your views here.




from django.http import JsonResponse


from django.shortcuts import render


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



