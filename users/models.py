from decimal import Decimal
from django.db import models
from django.contrib.auth.models import AbstractUser


class Service(models.Model):
    """Service categories - providers choose from these"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']


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
    
    # Rating fields
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0, null=True, blank=True)
    total_ratings = models.IntegerField(default=0)

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


class SuggestedService(models.Model):
    """When providers add new services not in list - automatically approved"""
    name = models.CharField(max_length=100, unique=True)
    suggested_by = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='suggested_services'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} (suggested by {self.suggested_by.username})"
    
    class Meta:
        ordering = ['-created_at']


class Rating(models.Model):
    """Client ratings for providers after job completion"""
    
    RATING_CHOICES = [
        (1, '⭐ 1 - Poor'),
        (2, '⭐⭐ 2 - Fair'),
        (3, '⭐⭐⭐ 3 - Good'),
        (4, '⭐⭐⭐⭐ 4 - Very Good'),
        (5, '⭐⭐⭐⭐⭐ 5 - Excellent'),
    ]
    
    service_request = models.OneToOneField(
        ServiceRequest,
        on_delete=models.CASCADE,
        related_name='rating'
    )
    provider = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_ratings'
    )
    client = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='given_ratings'
    )
    rating = models.IntegerField(choices=RATING_CHOICES)
    review = models.TextField(blank=True, help_text="Write your experience with this provider")
    is_approved = models.BooleanField(default=True, help_text="Admin can hide inappropriate reviews")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.client.username} rated {self.provider.username}: {self.rating} stars"
    
    @property
    def rating_percentage(self):
        return (self.rating / 5) * 100


class JobCompletion(models.Model):
    """Track when client confirms job completion"""
    
    service_request = models.OneToOneField(
        ServiceRequest,
        on_delete=models.CASCADE,
        related_name='completion'
    )
    client_confirmed = models.BooleanField(default=False)
    client_confirmed_at = models.DateTimeField(null=True, blank=True)
    provider_confirmed = models.BooleanField(default=False)
    provider_confirmed_at = models.DateTimeField(null=True, blank=True)
    client_feedback = models.TextField(blank=True)
    completed_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Completion for request #{self.service_request.id}"
    
    # ==================== HOMEPAGE CMS MODELS ====================

class HomepageSettings(models.Model):
    """Main homepage settings that admin can edit"""
    
    # Hero Section
    hero_title = models.CharField(max_length=200, default='Find Trusted Service Providers Near You')
    hero_subtitle = models.TextField(default='Connect with verified professionals for plumbing, electrical, cleaning, and more. Get quality service at fair prices.')
    hero_background_image = models.ImageField(upload_to='homepage/hero/', blank=True, null=True)
    hero_background_color = models.CharField(max_length=20, default='#2563eb', help_text='Hex color code')
    
    # Stats Section
    stats_visible = models.BooleanField(default=True)
    stats_background_color = models.CharField(max_length=20, default='#ffffff', blank=True)
    
    # Services Section
    services_title = models.CharField(max_length=200, default='Popular Services')
    services_subtitle = models.CharField(max_length=500, default='', blank=True)
    services_visible = models.BooleanField(default=True)
    
    # How It Works Section
    how_it_works_title = models.CharField(max_length=200, default='How It Works')
    how_it_works_visible = models.BooleanField(default=True)
    
    # Testimonials Section
    testimonials_title = models.CharField(max_length=200, default='What Our Customers Say')
    testimonials_visible = models.BooleanField(default=True)
    
    # CTA Section
    cta_title = models.CharField(max_length=200, default='Ready to Get Started?')
    cta_subtitle = models.CharField(max_length=500, default='Join thousands of satisfied customers and trusted providers')
    cta_button1_text = models.CharField(max_length=50, default='I Need a Service')
    cta_button2_text = models.CharField(max_length=50, default='Become a Provider')
    cta_visible = models.BooleanField(default=True)
    
    # Footer
    footer_copyright = models.CharField(max_length=200, default='© 2024 Buildimity. All rights reserved.')
    footer_email = models.EmailField(default='support@buildimity.com')
    footer_phone = models.CharField(max_length=50, default='+256 123 456 789')
    
    # SEO
    meta_description = models.TextField(default='Find trusted service providers in Uganda. Plumbing, electrical, cleaning, and more. Connect with verified professionals on Buildimity.', max_length=500)
    meta_keywords = models.CharField(max_length=500, default='service providers, plumbing, electrical, cleaning, home services, Uganda, Kampala')
    
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Homepage Settings"
    
    def __str__(self):
        return "Homepage Settings"
    
    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        if not self.pk and HomepageSettings.objects.exists():
            return  # Don't create duplicate
        super().save(*args, **kwargs)


class ServiceCard(models.Model):
    """Custom service cards for the homepage"""
    
    service = models.ForeignKey('Service', on_delete=models.CASCADE, null=True, blank=True)
    custom_name = models.CharField(max_length=100, blank=True, help_text="Leave blank to use service name")
    icon = models.CharField(max_length=50, default='fa-wrench', help_text='Font Awesome icon class')
    description = models.CharField(max_length=200, blank=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.display_name
    
    @property
    def display_name(self):
        if self.custom_name:
            return self.custom_name
        return self.service.name if self.service else 'Custom Service'


class Testimonial(models.Model):
    """Customer testimonials for homepage"""
    
    author_name = models.CharField(max_length=100)
    author_location = models.CharField(max_length=100, blank=True)
    content = models.TextField()
    rating = models.IntegerField(default=5, choices=[(1,1),(2,2),(3,3),(4,4),(5,5)])
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.author_name} - {self.author_location}"


class HomepageImage(models.Model):
    """Images for homepage banners and backgrounds"""
    
    SECTION_CHOICES = [
        ('hero', 'Hero Background'),
        ('services', 'Services Background'),
        ('testimonials', 'Testimonials Background'),
        ('cta', 'CTA Background'),
    ]
    
    section = models.CharField(max_length=50, choices=SECTION_CHOICES)
    image = models.ImageField(upload_to='homepage/')
    alt_text = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.get_section_display()}: {self.image.name}"


class IPWhitelistConfig(models.Model):
    """Store IP whitelist configuration in database"""
    service = models.CharField(max_length=50)
    environment = models.CharField(max_length=20)
    ip_address = models.GenericIPAddressField()
    description = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['service', 'environment', 'ip_address']
    
    def __str__(self):
        return f"{self.service} - {self.environment}: {self.ip_address}"