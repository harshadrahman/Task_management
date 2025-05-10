from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('user', 'user'),
    ]

    username = models.CharField(max_length=150, unique=True, null=True, blank=True)
    password = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(unique=True,null=True,blank=True)
    category = models.CharField(max_length=50, choices=ROLE_CHOICES,null=True,blank=True)
    parent_admin = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_users'
    )

    def __str__(self):
        return self.username

class Task(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In progress', 'In progress'),
        ('Completed', 'Completed'),
    ]

    title = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    assigned_to = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    due_date = models.DateTimeField(null=True,blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES,null=True,blank=True)
    completion_report = models.TextField(null=True, blank=True)
    hours = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.title