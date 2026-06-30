from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, UpdateRecordForm
from .models import Record
import logging

logger = logging.getLogger(__name__)

def home(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in.")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('home')
    else:
        records = Record.objects.all()
        context = {'records': records}
    return render(request, 'base/home.html', context)


def signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful. You can now log in.")
            return redirect('home')
        else:
            messages.error(request, "Registration failed. Please correct the errors below.")
            return render(request, 'base/register.html', {'form': form})
    else:
        form = RegisterForm()
        return render(request, 'base/register.html', {'form': form})
    return render(request, 'base/register.html')


def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('home')


def display_record(request, pk):
    if request.user.is_authenticated:
        customer_record = Record.objects.get(id=pk)
        return render(request, 'base/record.html', {'customer_record': customer_record})
    else:
        messages.error(request, "You must be logged in to view that page.")
        return redirect('home')
    return render(request, 'base/record.html') 


def delete_record(request, pk):
    if request.user.is_authenticated:
        customer_record = Record.objects.get(id=pk)
        customer_record.delete()
        messages.success(request, "Record deleted successfully.")
        return redirect('home')
    else:
        messages.error(request, "You must be logged in to perform that action.")
        return redirect('home')
    return render(request, 'base/record.html')


def update_record(request, pk):
    if request.user.is_authenticated:
        customer_record = Record.objects.get(id=pk)
        form = UpdateRecordForm(instance=customer_record)
        if request.method == 'POST':
            form = UpdateRecordForm(request.POST, instance=customer_record)
            if form.is_valid():
                form.save()
                messages.success(request, "Record updated successfully.")
                return redirect('home')
            else:
                messages.error(request, "Update failed. Please correct the errors below.")
                return render(request, 'base/update_record.html', {'form': form})
        else:
            return render(request, 'base/update_record.html', {'form': form})
    return render(request, 'base/update_record.html')


@login_required
def add_record(request):
    if request.method == 'POST':
        form = UpdateRecordForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Record added successfully.")
            logger.info('record added successfully')
            return redirect('home')
        else:
            messages.error(request, "Failed to add record. Please correct the errors below.")
            return render(request, 'base/add_record.html', {'form': form})
    else:
        form = UpdateRecordForm()
    return render(request, 'base/add_record.html')