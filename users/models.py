from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    CLIENT = 'client'
    PROVIDER = 'provider'

    ROLE_CHOICES = [
        (CLIENT, 'Client'),
        (PROVIDER, 'Service Provider'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=CLIENT)
    service_name = models.CharField(max_length=100, blank=True)
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