from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # address: models.CharField(max_length=255, blank=True)
#    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username

class Complaint(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    message = models.TextField()
    email = models.EmailField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Complaint by {self.user.username} - {self.subject}"