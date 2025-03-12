from django.contrib import admin
from .models import Car, CarSighting, Alert, Report, Location

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('number_plate', 'status', 'registered_on', 'last_updated')
    list_filter = ('status', 'registered_on')
    search_fields = ('number_plate',)

@admin.register(CarSighting)
class CarSightingAdmin(admin.ModelAdmin):
    list_display = ('car', 'location', 'timestamp')
    list_filter = ('location', 'timestamp')
    search_fields = ('car__number_plate',)

@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ('alert_type', 'car', 'timestamp', 'is_read')
    list_filter = ('alert_type', 'is_read', 'timestamp')
    search_fields = ('car__number_plate', 'message')

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'report_type', 'created_by', 'created_at')
    list_filter = ('report_type', 'created_at')
    search_fields = ('title', 'created_by__username')

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

