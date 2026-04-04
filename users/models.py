from decimal import Decimal

from django.db import models
from django.contrib.auth.models import AbstractUser


class Service(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class User(AbstractUser):
    CLIENT = 'client'
    PROVIDER = 'provider'
    ADMIN = 'admin'

    ROLE_CHOICES = [
        (CLIENT, 'Client'),
        (PROVIDER, 'Service Provider'),
        (ADMIN, 'Admin'),
    ]

    MTN = 'mtn'
    AIRTEL = 'airtel'

    PAYMENT_NETWORK_CHOICES = [
        (MTN, 'MTN Mobile Money'),
        (AIRTEL, 'Airtel Money'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=CLIENT)
    service = models.ForeignKey(
        Service,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='providers'
    )
    phone_number = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    profile_photo = models.ImageField(upload_to='provider_profiles/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    is_suspended = models.BooleanField(default=False)

    # payout/payment details
    preferred_payment_network = models.CharField(
        max_length=20,
        choices=PAYMENT_NETWORK_CHOICES,
        blank=True
    )
    mobile_money_number = models.CharField(max_length=20, blank=True)
    account_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)

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


class AdminNotification(models.Model):
    UNLISTED_SERVICE = 'unlisted_service'
    NEW_PROVIDER = 'new_provider'
    PAYMENT = 'payment'
    GENERAL = 'general'

    TYPE_CHOICES = [
        (UNLISTED_SERVICE, 'Unlisted Service'),
        (NEW_PROVIDER, 'New Provider'),
        (PAYMENT, 'Payment'),
        (GENERAL, 'General'),
    ]

    title = models.CharField(max_length=255)
    message = models.TextField()
    notification_type = models.CharField(max_length=30, choices=TYPE_CHOICES, default=GENERAL)
    is_read = models.BooleanField(default=False)
    related_user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='admin_notifications'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ClientServiceNeed(models.Model):
    OPEN = 'open'
    MATCHED = 'matched'
    NEGOTIATING = 'negotiating'
    AGREED = 'agreed'
    PAID = 'paid'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'

    STATUS_CHOICES = [
        (OPEN, 'Open'),
        (MATCHED, 'Matched'),
        (NEGOTIATING, 'Negotiating'),
        (AGREED, 'Agreed'),
        (PAID, 'Paid'),
        (IN_PROGRESS, 'In Progress'),
        (COMPLETED, 'Completed'),
        (CANCELLED, 'Cancelled'),
    ]

    client = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='service_needs'
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='client_needs'
    )
    custom_service_name = models.CharField(max_length=120, blank=True)
    description = models.TextField()
    budget = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    location = models.CharField(max_length=255, blank=True)
    preferred_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=OPEN)
    admin_notified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_unlisted_service(self):
        return not self.service and bool(self.custom_service_name)

    def service_display(self):
        if self.service:
            return self.service.name
        return self.custom_service_name or "Unknown service"

    def __str__(self):
        return f"{self.client.username} needs {self.service_display()}"


class ServiceRequest(models.Model):
    PENDING = 'pending'
    NEGOTIATING = 'negotiating'
    AGREED = 'agreed'
    PAID = 'paid'
    IN_PROGRESS = 'in_progress'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (NEGOTIATING, 'Negotiating'),
        (AGREED, 'Agreed'),
        (PAID, 'Paid'),
        (IN_PROGRESS, 'In Progress'),
        (ACCEPTED, 'Accepted'),
        (REJECTED, 'Rejected'),
        (COMPLETED, 'Completed'),
        (CANCELLED, 'Cancelled'),
    ]

    client = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_service_requests'
    )
    provider = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_service_requests'
    )
    service_need = models.ForeignKey(
        ClientServiceNeed,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='service_requests'
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='service_requests'
    )
    message = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=PENDING
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )
    commission = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )
    provider_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    client_confirmed = models.BooleanField(default=False)
    provider_confirmed = models.BooleanField(default=False)

    accepted_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        amount = self.amount or Decimal("0")
        if amount > 0:
            self.commission = amount * Decimal("0.10")
            self.provider_amount = amount - self.commission
        else:
            self.commission = Decimal("0")
            self.provider_amount = Decimal("0")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.client.username} -> {self.provider.username} ({self.status})"


class Negotiation(models.Model):
    service_request = models.ForeignKey(
        ServiceRequest,
        on_delete=models.CASCADE,
        related_name='negotiations'
    )
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_negotiations'
    )
    message = models.TextField(blank=True)
    proposed_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Negotiation for request #{self.service_request.id}"


class Payment(models.Model):
    MTN = 'mtn'
    AIRTEL = 'airtel'

    METHOD_CHOICES = [
        (MTN, 'MTN Mobile Money'),
        (AIRTEL, 'Airtel Money'),
    ]

    PENDING = 'pending'
    PAID = 'paid'
    FAILED = 'failed'
    HELD = 'held'
    RELEASED = 'released'
    REFUNDED = 'refunded'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (PAID, 'Paid'),
        (FAILED, 'Failed'),
        (HELD, 'Held by Platform'),
        (RELEASED, 'Released to Provider'),
        (REFUNDED, 'Refunded'),
    ]

    service_request = models.OneToOneField(
        ServiceRequest,
        on_delete=models.CASCADE,
        related_name='payment'
    )
    client = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='payments_made'
    )
    provider = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='payments_received_for_jobs'
    )

    method = models.CharField(max_length=20, choices=METHOD_CHOICES)
    payer_phone_number = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    commission = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    provider_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    transaction_id = models.CharField(max_length=120, blank=True)
    external_reference = models.CharField(max_length=120, blank=True)

    paid_at = models.DateTimeField(null=True, blank=True)
    released_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        amount = self.amount or Decimal("0")
        if amount > 0:
            self.commission = amount * Decimal("0.10")
            self.provider_amount = amount - self.commission
        else:
            self.commission = Decimal("0")
            self.provider_amount = Decimal("0")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Payment for request #{self.service_request.id} - {self.status}"