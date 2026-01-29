from django.contrib import admin
from .models import CustomUser, Complaint, StatusHistory

# Register your models here.

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'user', 'category', 'status', 'created_at', 'updated_at']
    list_filter = ['status', 'category', 'created_at', 'updated_at']
    search_fields = ['title', 'description', 'user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at', 'resolved_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Complaint Information', {
            'fields': ('title', 'description', 'category', 'user')
        }),
        ('Status Information', {
            'fields': ('status', 'resolved_by', 'resolved_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(StatusHistory)
class StatusHistoryAdmin(admin.ModelAdmin):
    list_display = ['complaint', 'old_status', 'new_status', 'changed_by', 'changed_at']
    list_filter = ['old_status', 'new_status', 'changed_at']
    search_fields = ['complaint__title', 'changed_by__username', 'notes']
    readonly_fields = ['changed_at']
    ordering = ['-changed_at']

# Customize the existing CustomUser admin if needed
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_staff', 'is_superuser', 'date_joined']
    list_filter = ['is_staff', 'is_superuser', 'date_joined']
    search_fields = ['username', 'email']
