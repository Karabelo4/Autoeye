from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import scan_vehicle

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Authentication
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Car management
    path('cars/search/', views.search_view, name='search'),
    path('cars/<int:pk>/', views.car_detail, name='car_detail'),
    path('cars/add/', views.add_car, name='add_car'),
    path('cars/<int:pk>/edit/', views.edit_car, name='edit_car'),
    path('cars/<int:pk>/mark-stolen/', views.mark_as_stolen, name='mark_as_stolen'),
    
    # Sightings
    path('sightings/add/', views.add_sighting, name='add_sighting'),
    
    # Alerts
    path('alerts/', views.alerts_view, name='alerts'),
    path('alerts/<int:pk>/mark-read/', views.mark_alert_read, name='mark_alert_read'),
    
    # Statistics
    path('statistics/', views.statistics_view, name='statistics'),
    
    # Reports
    path('reports/', views.reports_view, name='reports'),
    path('reports/create/', views.create_report, name='create_report'),
    
    # License Plate Scanning
    path('scan/', scan_vehicle, name='scan_vehicle'),
    
    # Search functionality
    path('search/', views.search_page, name='search_page'),
    path('api/vehicle/', views.search_vehicle, name='search_vehicle'),
]