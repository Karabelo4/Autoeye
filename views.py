from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
import json
import csv
import matplotlib.pyplot as plt
import io
import base64
from django.views.decorators.http import require_http_methods

from .models import Car, CarSighting, Alert, Report, VehicleRecord, StolenVehicle, CameraLocation, Vehicle, Sighting
from .forms import CarForm, CarSightingForm, SearchForm, ReportForm, CustomAuthenticationForm
from .lpr import detect_license_plate

default_template_path = 'car_management/'

class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = f'{default_template_path}login.html'

@login_required
def dashboard(request):
    recent_sightings = CarSighting.objects.all().order_by('-timestamp')[:5]
    stolen_cars_count = Car.objects.filter(status='stolen').count()
    unread_alerts_count = Alert.objects.filter(is_read=False).count()
    
    context = {
        'recent_sightings': recent_sightings,
        'unread_alerts_count': unread_alerts_count,
        'stolen_cars_count': stolen_cars_count,
    }
    return render(request, f'{default_template_path}dashboard.html', context)

@login_required
def search_view(request):
    form = SearchForm(request.GET or None)
    cars = Car.objects.all()
    
    if form.is_valid():
        number_plate = form.cleaned_data.get('number_plate')
        status = form.cleaned_data.get('status')
        date_from = form.cleaned_data.get('date_from')
        date_to = form.cleaned_data.get('date_to')
        
        if number_plate:
            cars = cars.filter(number_plate__icontains=number_plate)
        if status:
            cars = cars.filter(status=status)
        if date_from and date_to:
            cars = cars.filter(registered_on__range=[date_from, date_to])
    
    return render(request, f'{default_template_path}search.html', {'form': form, 'cars': cars})

@login_required
def car_detail(request, pk):
    car = get_object_or_404(Car, pk=pk)
    return render(request, f'{default_template_path}car_detail.html', {'car': car, 'sightings': car.sightings.all().order_by('-timestamp')})

@login_required
def add_car(request):
    form = CarForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        car = form.save()
        messages.success(request, f'Car with number plate {car.number_plate} has been added.')
        return redirect('car_detail', pk=car.pk)
    
    return render(request, f'{default_template_path}car_form.html', {'form': form, 'title': 'Add New Car'})

@login_required
def mark_as_stolen(request, pk):
    car = get_object_or_404(Car, pk=pk)
    car.status = 'stolen'
    car.save()
    Alert.objects.create(car=car, alert_type='stolen', message=f'Car {car.number_plate} marked as stolen.')
    messages.warning(request, f'Car {car.number_plate} marked as stolen.')
    return redirect('car_detail', pk=car.pk)

@login_required
def statistics_view(request):
    status_stats = Car.objects.values('status').annotate(count=Count('status'))
    today, one_year_ago = timezone.now().date(), timezone.now().date() - timedelta(days=365)
    
    monthly_sightings = [
        {'month': (one_year_ago + timedelta(days=30*i)).strftime('%b %Y'),
         'count': CarSighting.objects.filter(timestamp__date__range=[one_year_ago + timedelta(days=30*i), one_year_ago + timedelta(days=30*(i+1))]).count()}
        for i in range(12)
    ]
    
    return render(request, f'{default_template_path}statistics.html', {
        'status_stats': status_stats,
        'monthly_sightings': monthly_sightings,
    })

@require_http_methods(["GET"])
def search_vehicle(request):
    license_plate = request.GET.get('plate', '').strip().upper()
    if not license_plate:
        return JsonResponse({'error': 'License plate required'}, status=400)
    try:
        vehicle = Vehicle.objects.get(license_plate=license_plate)
        sightings = Sighting.objects.filter(vehicle=vehicle).order_by('-timestamp')
        return JsonResponse({
            'id': vehicle.id,
            'licensePlate': vehicle.license_plate,
            'make': vehicle.make,
            'model': vehicle.model,
            'year': vehicle.year,
            'color': vehicle.color,
            'status': vehicle.status,
            'sightings': [{'timestamp': s.timestamp.isoformat(), 'location': s.location} for s in sightings]
        })
    except Vehicle.DoesNotExist:
        return JsonResponse({'error': 'Vehicle not found'}, status=404)

@login_required
def scan_vehicle(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        plate_number = detect_license_plate(image)
        
        if plate_number:
            vehicle = VehicleRecord.objects.filter(license_plate=plate_number).first()
            stolen = StolenVehicle.objects.filter(license_plate=plate_number).first()
            message = f"⚠️ Alert! Stolen Vehicle Detected: {stolen.license_plate}" if stolen else f"✅ Vehicle Verified: {plate_number}"
            return render(request, 'scan_result.html', {'message': message, 'plate_number': plate_number})
    
    return render(request, 'scan_vehicle.html')
