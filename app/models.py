from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class CustomUser(AbstractUser):
    # address: models.CharField(max_length=255, blank=True)
#    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username

<<<<<<< HEAD
    @property
    def is_admin(self):
        """Check if user has admin privileges"""
        return self.is_staff or self.is_superuser


class Complaint(models.Model):
    CATEGORY_CHOICES = [
        ('technical', 'Technical Issue'),
        ('service', 'Service Quality'),
        ('billing', 'Billing Issue'),
        ('general', 'General Feedback'),
    ]
    
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
    ]
    
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='complaints')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='resolved_complaints')
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Complaint'
        verbose_name_plural = 'Complaints'

    def __str__(self):
        return f"{self.title} - {self.get_status_display()}"

    def can_be_edited(self):
        """Check if complaint can be edited by user"""
        return self.status != 'resolved'

    def mark_resolved(self, admin_user):
        """Mark complaint as resolved"""
        self.status = 'resolved'
        self.resolved_by = admin_user
        self.resolved_at = timezone.now()
        self.save()


class StatusHistory(models.Model):
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name='status_history')
    old_status = models.CharField(max_length=20)
    new_status = models.CharField(max_length=20)
    changed_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    changed_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-changed_at']
        verbose_name = 'Status History'
        verbose_name_plural = 'Status Histories'

    def __str__(self):
        return f"{self.complaint.title}: {self.old_status} → {self.new_status}"

=======
class Complaint(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    message = models.TextField()
    email = models.EmailField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)  # To track if the complaint is resolved

    def __str__(self):
        return f"Complaint by {self.user.username} - {self.subject}"
>>>>>>> origin/main
