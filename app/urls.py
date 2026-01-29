from django.contrib import admin
from django.urls import path
from .views import (
    login_view, signup_view, logout_view, user_detail_view,
    # User complaint views
    complaint_list_view, complaint_detail_view, complaint_create_view, 
    complaint_update_view, user_dashboard_view,
    # Admin complaint views
    admin_complaint_list_view, admin_complaint_detail_view, 
    complaint_status_update_view, complaint_delete_view, admin_dashboard_view
)

urlpatterns = [
    # Authentication URLs
    path("", signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name="logout"),
    path('user/<int:pk>/', user_detail_view, name='user_detail'),
    
    # User Dashboard
    path('dashboard/', user_dashboard_view, name='user_dashboard'),
    
    # User Complaint URLs
    path('complaints/', complaint_list_view, name='complaint_list'),
    path('complaints/create/', complaint_create_view, name='complaint_create'),
    path('complaints/<int:complaint_id>/', complaint_detail_view, name='complaint_detail'),
    path('complaints/<int:complaint_id>/edit/', complaint_update_view, name='complaint_update'),
    
    # Admin URLs (changed from 'admin/' to 'management/' to avoid conflict)
    path('management/dashboard/', admin_dashboard_view, name='admin_dashboard'),
    path('management/complaints/', admin_complaint_list_view, name='admin_complaint_list'),
    path('management/complaints/<int:complaint_id>/', admin_complaint_detail_view, name='admin_complaint_detail'),
    path('management/complaints/<int:complaint_id>/status/', complaint_status_update_view, name='complaint_status_update'),
    path('management/complaints/<int:complaint_id>/delete/', complaint_delete_view, name='complaint_delete'),
]
