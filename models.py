from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Location(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class CameraLocation(models.Model):
    camera_id = models.CharField(max_length=50, unique=True)
    location = models.CharField(max_length=255)

    def __str__(self):
        return f"Camera {self.camera_id} at {self.location}"

class Car(models.Model):
    STATUS_CHOICES = [
        ('normal', 'Normal'),
        ('stolen', 'Stolen'),
        ('suspicious', 'Suspicious'),
    ]
    
    number_plate = models.CharField(max_length=20, unique=True)
    driver_image = models.ImageField(upload_to='driver_images/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='normal')
    registered_on = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.number_plate

class CarSighting(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='sightings')
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to='sighting_images/', blank=True, null=True)

    def __str__(self):
        return f"{self.car.number_plate} at {self.location.name} on {self.timestamp}"

class Alert(models.Model):
    ALERT_TYPES = [
        ('stolen', 'Stolen Vehicle'),
        ('suspicious', 'Suspicious Vehicle'),
        ('system', 'System Alert'),
    ]

    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='alerts', null=True, blank=True)
    alert_type = models.CharField(max_length=20, choices=ALERT_TYPES)
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.alert_type} - {self.timestamp}"

class Report(models.Model):
    REPORT_TYPES = [
        ('daily', 'Daily Report'),
        ('weekly', 'Weekly Report'),
        ('monthly', 'Monthly Report'),
        ('custom', 'Custom Report'),
    ]

    title = models.CharField(max_length=100)
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField()
    end_date = models.DateField()
    file = models.FileField(upload_to='reports/', blank=True, null=True)

    def __str__(self):
        return self.title

class VehicleImage(models.Model):
    vehicle_name = models.CharField(max_length=100)
    image = models.BinaryField()  # Store image as binary data

    def __str__(self):
        return self.vehicle_name

class Vehicle(models.Model):
    STATUS_CHOICES = (
        ('normal', 'Normal'),
        ('stolen', 'Stolen'),
        ('suspicious', 'Suspicious'),
    )
    
    license_plate = models.CharField(max_length=20, unique=True)
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.IntegerField()
    color = models.CharField(max_length=30)
    vin = models.CharField(max_length=17, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='normal')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.license_plate} - {self.make} {self.model}"

class Camera(models.Model):
    STATUS_CHOICES = (
        ('online', 'Online'),
        ('offline', 'Offline'),
        ('maintenance', 'Maintenance'),
    )
    
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='online')
    last_activity = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.location}"

class Sighting(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='sightings')
    camera = models.ForeignKey(Camera, on_delete=models.SET_NULL, null=True, related_name='sightings')
    timestamp = models.DateTimeField()
    location = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    direction = models.CharField(max_length=50, blank=True, null=True)
    speed = models.FloatField(blank=True, null=True)
    image = models.ImageField(upload_to='sightings/', blank=True, null=True)
    
    def __str__(self):
        return f"{self.vehicle.license_plate} at {self.location} on {self.timestamp}"

class StolenVehicle(models.Model):
    license_plate = models.CharField(max_length=20, unique=True)
    reported_date = models.DateTimeField(auto_now_add=True)
    last_seen_location = models.ForeignKey(CameraLocation, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Stolen: {self.license_plate}"
