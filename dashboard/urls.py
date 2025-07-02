from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='admin-dashboard'),
    path('dashboard/bookings/', views.bookings_analysis, name='dashboard-bookings-analysis'),
    path('dashboard/revenue/', views.revenue_analysis, name='dashboard-revenue-analysis'),
    path('dashboard/users/', views.user_insights, name='dashboard-user-insights'),
    path('dashboard/bookings/export-csv/', views.bookings_export_csv, name='dashboard-bookings-export-csv'),
    path('dashboard/revenue/export-csv/', views.revenue_export_csv, name='dashboard-revenue-export-csv'),
    path('dashboard/bookings/city/', views.bookings_by_city_analytics, name='dashboard-bookings-by-city'),
    path('dashboard/bookings/city/export-csv/', views.bookings_by_city_export_csv, name='dashboard-bookings-by-city-export-csv'),
]