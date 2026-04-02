from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    CLIENT = 'client'
    PROVIDER = 'provider'
    ADMIN = 'admin'

    ROLE_CHOICES = [
        (CLIENT, 'Client'),
        (PROVIDER, 'Service Provider'),
        (ADMIN, 'Admin'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=CLIENT)
    service = models.ForeignKey('Service', on_delete=models.SET_NULL, null=True, blank=True, related_name='providers')
    phone_number = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    profile_photo = models.ImageField(upload_to='provider_profiles/', blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.role})"


class ProviderWorkImage(models.Model):
    provider = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='work_images'
    )
    image = models.ImageField(upload_to='provider_work/')
    caption = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.provider.username} work image"


class ProviderSearch(models.Model):
    client = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='searches'
    )
    query = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client.username} searched for {self.query}"
    

    from django.db import models
from django.contrib.auth.models import AbstractUser


class Service(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name