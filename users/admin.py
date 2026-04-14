from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.urls import path
from django.shortcuts import redirect, render
from django.contrib import messages
from django.utils.html import format_html
from django.utils import timezone
from django.db.models import Sum, Count, Q
from django.http import HttpResponseRedirect
from django.urls import reverse
from decimal import Decimal

from .models import (
    User,
    Service,
    ProviderWorkImage,
    ProviderSearch,
    ServiceRequest,
    ClientServiceNeed,
    Negotiation,
    Payment,
    AdminNotification,
    HomepageSettings,  # Add this
    ServiceCard,       # Add this
    Testimonial,       # Add this
    HomepageImage,     # Add this
)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        'username',
        'email',
        'role',
        'service',
        'phone_number',
        'preferred_payment_network',
        'mobile_money_number',
        'account_balance',
        'is_verified',
        'is_suspended',
        'admin_actions_display',
        'is_staff',
        'is_active',
        'date_joined',
    )

    list_filter = (
        'role',
        'service',
        'preferred_payment_network',
        'is_verified',
        'is_suspended',
        'is_staff',
        'is_active',
    )

    search_fields = (
        'username',
        'email',
        'first_name',
        'last_name',
        'phone_number',
        'mobile_money_number',
        'location',
    )

    ordering = ('-date_joined',)
    list_editable = ('is_verified', 'is_suspended')
    
    actions = ['verify_providers', 'suspend_users', 'unsuspend_users']
    
    fieldsets = UserAdmin.fieldsets + (
        ("Marketplace Info", {
            'fields': (
                'role',
                'service',
                'phone_number',
                'location',
                'bio',
                'profile_photo',
                'is_verified',
                'is_suspended',
            )
        }),
        ("Payment Info", {
            'fields': (
                'preferred_payment_network',
                'mobile_money_number',
                'account_balance',
            ),
            'classes': ('collapse',)
        }),
    )
    
    def admin_actions_display(self, obj):
        """Display action buttons in admin list view"""
        buttons = []
        
        if obj.role == 'provider' and not obj.is_verified:
            buttons.append(f'<a class="button" href="/admin/verify-user/{obj.id}/" style="background: #28a745; color: white; padding: 3px 8px; text-decoration: none; border-radius: 3px; margin: 2px;">✓ Verify</a>')
        
        if obj.is_suspended:
            buttons.append(f'<a class="button" href="/admin/unsuspend-user/{obj.id}/" style="background: #ffc107; color: black; padding: 3px 8px; text-decoration: none; border-radius: 3px; margin: 2px;">🔓 Unsuspend</a>')
        else:
            buttons.append(f'<a class="button" href="/admin/suspend-user/{obj.id}/" style="background: #dc3545; color: white; padding: 3px 8px; text-decoration: none; border-radius: 3px; margin: 2px;">🔒 Suspend</a>')
        
        buttons.append(f'<a class="button" href="/admin/adjust-balance/{obj.id}/" style="background: #17a2b8; color: white; padding: 3px 8px; text-decoration: none; border-radius: 3px; margin: 2px;">💰 Adjust Balance</a>')
        
        return format_html(' '.join(buttons))
    admin_actions_display.short_description = 'Actions'
    admin_actions_display.allow_tags = True
    
    def verify_providers(self, request, queryset):
        count = queryset.filter(role='provider', is_verified=False).update(is_verified=True)
        self.message_user(request, f'{count} provider(s) verified successfully.')
    verify_providers.short_description = "Verify selected providers"
    
    def suspend_users(self, request, queryset):
        count = queryset.update(is_suspended=True)
        self.message_user(request, f'{count} user(s) suspended.')
    suspend_users.short_description = "Suspend selected users"
    
    def unsuspend_users(self, request, queryset):
        count = queryset.update(is_suspended=False)
        self.message_user(request, f'{count} user(s) unsuspended.')
    unsuspend_users.short_description = "Unsuspend selected users"
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('verify-user/<int:user_id>/', self.admin_site.admin_view(self.verify_user), name='verify-user'),
            path('suspend-user/<int:user_id>/', self.admin_site.admin_view(self.suspend_user), name='suspend-user'),
            path('unsuspend-user/<int:user_id>/', self.admin_site.admin_view(self.unsuspend_user), name='unsuspend-user'),
            path('adjust-balance/<int:user_id>/', self.admin_site.admin_view(self.adjust_balance), name='adjust-balance'),
        ]
        return custom_urls + urls
    
    def verify_user(self, request, user_id):
        user = User.objects.get(id=user_id)
        user.is_verified = True
        user.save()
        self.message_user(request, f'{user.username} verified successfully.')
        return redirect('admin:users_user_changelist')
    
    def suspend_user(self, request, user_id):
        user = User.objects.get(id=user_id)
        user.is_suspended = True
        user.save()
        self.message_user(request, f'{user.username} suspended.')
        return redirect('admin:users_user_changelist')
    
    def unsuspend_user(self, request, user_id):
        user = User.objects.get(id=user_id)
        user.is_suspended = False
        user.save()
        self.message_user(request, f'{user.username} unsuspended.')
        return redirect('admin:users_user_changelist')
    
    def adjust_balance(self, request, user_id):
        user = User.objects.get(id=user_id)
        if request.method == 'POST':
            amount = Decimal(request.POST.get('amount', 0))
            operation = request.POST.get('operation', 'add')
            
            if operation == 'add':
                user.account_balance += amount
                message = f'Added {amount} to balance'
            else:
                user.account_balance -= amount
                message = f'Subtracted {amount} from balance'
            
            user.save()
            self.message_user(request, f'{message} for {user.username}. New balance: {user.account_balance}')
            return redirect('admin:users_user_changelist')
        
        context = {
            'title': f'Adjust Balance for {user.username}',
            'user': user,
            'current_balance': user.account_balance,
        }
        return render(request, 'admin/adjust_balance.html', context)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'provider_count', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')
    ordering = ('name',)
    list_editable = ('is_active',)
    
    def provider_count(self, obj):
        return obj.providers.filter(role='provider').count()
    provider_count.short_description = '# Providers'


@admin.register(ProviderWorkImage)
class ProviderWorkImageAdmin(admin.ModelAdmin):
    list_display = ('provider', 'image_preview', 'caption', 'uploaded_at')
    search_fields = ('provider__username', 'caption')
    list_filter = ('uploaded_at',)
    ordering = ('-uploaded_at',)
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.image.url)
        return '-'
    image_preview.short_description = 'Preview'


@admin.register(ProviderSearch)
class ProviderSearchAdmin(admin.ModelAdmin):
    list_display = ('client', 'query', 'created_at')
    search_fields = ('client__username', 'query')
    list_filter = ('created_at',)
    ordering = ('-created_at',)


@admin.register(AdminNotification)
class AdminNotificationAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'notification_type',
        'related_user',
        'is_read',
        'created_at',
    )
    search_fields = ('title', 'message', 'related_user__username')
    list_filter = ('notification_type', 'is_read', 'created_at')
    ordering = ('-created_at',)
    list_editable = ('is_read',)
    actions = ['mark_as_read', 'mark_as_unread']
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
        self.message_user(request, f'{queryset.count()} notification(s) marked as read.')
    mark_as_read.short_description = "Mark selected as read"
    
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
        self.message_user(request, f'{queryset.count()} notification(s) marked as unread.')
    mark_as_unread.short_description = "Mark selected as unread"


@admin.register(ClientServiceNeed)
class ClientServiceNeedAdmin(admin.ModelAdmin):
    list_display = (
        'client',
        'service_display',
        'budget',
        'location',
        'status',
        'admin_notified',
        'created_at',
    )
    search_fields = (
        'client__username',
        'service__name',
        'custom_service_name',
        'description',
        'location',
    )
    list_filter = ('status', 'admin_notified', 'service', 'created_at')
    ordering = ('-created_at',)
    list_editable = ('status',)
    
    def service_display(self, obj):
        if obj.service:
            return obj.service.name
        return obj.custom_service_name or '-'
    service_display.short_description = 'Service'


@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'client',
        'provider',
        'service_display',
        'get_status',
        'amount',
        'commission',
        'provider_amount',
        'created_at',
        'quick_actions',
    )
    search_fields = (
        'client__username',
        'provider__username',
        'service__name',
        'message',
    )
    list_filter = ('status', 'service', 'created_at', 'accepted_at', 'completed_at')
    ordering = ('-created_at',)
    
    actions = ['mark_as_completed', 'mark_as_cancelled', 'recalculate_commission']
    
    def service_display(self, obj):
        if obj.service:
            return obj.service.name
        if obj.service_need:
            return obj.service_need.service_display()
        return '-'
    service_display.short_description = 'Service'
    
    def get_status(self, obj):
        colors = {
            'pending': 'orange',
            'negotiating': 'gold',
            'agreed': 'blue',
            'paid': 'green',
            'in_progress': 'purple',
            'accepted': 'teal',
            'rejected': 'red',
            'completed': 'darkgreen',
            'cancelled': 'darkred',
        }
        color = colors.get(obj.status, 'black')
        return format_html('<span style="color: {}; font-weight: bold;">{}</span>', color, obj.status.upper())
    get_status.short_description = 'Status'
    
    def quick_actions(self, obj):
        buttons = []
        if obj.status != 'completed':
            buttons.append(f'<a href="/admin/complete-request/{obj.id}/" style="background: #28a745; color: white; padding: 3px 8px; text-decoration: none; border-radius: 3px;">✓ Complete</a>')
        if obj.status != 'cancelled':
            buttons.append(f'<a href="/admin/cancel-request/{obj.id}/" style="background: #dc3545; color: white; padding: 3px 8px; text-decoration: none; border-radius: 3px;">✗ Cancel</a>')
        return format_html(' '.join(buttons))
    quick_actions.short_description = 'Actions'
    
    def mark_as_completed(self, request, queryset):
        count = queryset.update(status='completed', completed_at=timezone.now())
        self.message_user(request, f'{count} request(s) marked as completed.')
    mark_as_completed.short_description = "Mark selected as completed"
    
    def mark_as_cancelled(self, request, queryset):
        count = queryset.update(status='cancelled')
        self.message_user(request, f'{count} request(s) cancelled.')
    mark_as_cancelled.short_description = "Cancel selected requests"
    
    def recalculate_commission(self, request, queryset):
        for req in queryset:
            req.save()
        self.message_user(request, f'Commission recalculated for {queryset.count()} request(s).')
    recalculate_commission.short_description = "Recalculate commission"
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('complete-request/<int:request_id>/', self.admin_site.admin_view(self.complete_request), name='complete-request'),
            path('cancel-request/<int:request_id>/', self.admin_site.admin_view(self.cancel_request), name='cancel-request'),
        ]
        return custom_urls + urls
    
    def complete_request(self, request, request_id):
        service_request = ServiceRequest.objects.get(id=request_id)
        service_request.status = 'completed'
        service_request.completed_at = timezone.now()
        service_request.save()
        self.message_user(request, f'Request #{request_id} marked as completed.')
        return redirect('admin:users_servicerequest_changelist')
    
    def cancel_request(self, request, request_id):
        service_request = ServiceRequest.objects.get(id=request_id)
        service_request.status = 'cancelled'
        service_request.save()
        self.message_user(request, f'Request #{request_id} cancelled.')
        return redirect('admin:users_servicerequest_changelist')


@admin.register(Negotiation)
class NegotiationAdmin(admin.ModelAdmin):
    list_display = (
        'service_request',
        'sender',
        'proposed_price',
        'accepted',
        'created_at',
    )
    search_fields = (
        'service_request__id',
        'sender__username',
        'message',
    )
    list_filter = ('accepted', 'created_at')
    ordering = ('-created_at',)
    list_editable = ('accepted',)
    
    actions = ['accept_negotiations']
    
    def accept_negotiations(self, request, queryset):
        count = queryset.update(accepted=True)
        self.message_user(request, f'{count} negotiation(s) accepted.')
    accept_negotiations.short_description = "Accept selected negotiations"


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'service_request',
        'client',
        'provider',
        'method',
        'amount',
        'commission',
        'provider_amount',
        'get_status',
        'created_at',
        'payment_actions',
    )
    search_fields = (
        'service_request__id',
        'client__username',
        'provider__username',
        'payer_phone_number',
        'transaction_id',
        'external_reference',
    )
    list_filter = ('method', 'status', 'created_at', 'paid_at', 'released_at')
    ordering = ('-created_at',)
    
    actions = ['release_payments', 'refund_payments', 'mark_as_paid']
    
    def get_status(self, obj):
        colors = {
            'pending': 'orange',
            'paid': 'green',
            'failed': 'red',
            'held': 'blue',
            'released': 'purple',
            'refunded': 'darkred',
        }
        color = colors.get(obj.status, 'black')
        return format_html('<span style="color: {}; font-weight: bold;">{}</span>', color, obj.status.upper())
    get_status.short_description = 'Status'
    
    def payment_actions(self, obj):
        buttons = []
        if obj.status == 'held':
            buttons.append(f'<a href="/admin/release-payment/{obj.id}/" style="background: #28a745; color: white; padding: 3px 8px; text-decoration: none; border-radius: 3px;">💰 Release</a>')
        if obj.status in ['paid', 'held']:
            buttons.append(f'<a href="/admin/refund-payment/{obj.id}/" style="background: #dc3545; color: white; padding: 3px 8px; text-decoration: none; border-radius: 3px;">↺ Refund</a>')
        return format_html(' '.join(buttons))
    payment_actions.short_description = 'Actions'
    
    def release_payments(self, request, queryset):
        count = 0
        for payment in queryset:
            if payment.status == 'held':
                payment.status = 'released'
                payment.released_at = timezone.now()
                payment.save()
                payment.provider.account_balance += payment.provider_amount
                payment.provider.save()
                count += 1
        self.message_user(request, f'{count} payment(s) released to providers.')
    release_payments.short_description = "Release selected payments"
    
    def refund_payments(self, request, queryset):
        count = 0
        for payment in queryset:
            if payment.status in ['paid', 'held']:
                payment.status = 'refunded'
                payment.save()
                payment.client.account_balance += payment.amount
                payment.client.save()
                count += 1
        self.message_user(request, f'{count} payment(s) refunded.')
    refund_payments.short_description = "Refund selected payments"
    
    def mark_as_paid(self, request, queryset):
        count = queryset.update(status='paid', paid_at=timezone.now())
        self.message_user(request, f'{count} payment(s) marked as paid.')
    mark_as_paid.short_description = "Mark selected as paid"
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('release-payment/<int:payment_id>/', self.admin_site.admin_view(self.release_payment), name='release-payment'),
            path('refund-payment/<int:payment_id>/', self.admin_site.admin_view(self.refund_payment), name='refund-payment'),
        ]
        return custom_urls + urls
    
    def release_payment(self, request, payment_id):
        payment = Payment.objects.get(id=payment_id)
        if payment.status == 'held':
            payment.status = 'released'
            payment.released_at = timezone.now()
            payment.save()
            payment.provider.account_balance += payment.provider_amount
            payment.provider.save()
            self.message_user(request, f'Payment {payment_id} released to provider.')
        return redirect('admin:users_payment_changelist')
    
    def refund_payment(self, request, payment_id):
        payment = Payment.objects.get(id=payment_id)
        if payment.status in ['paid', 'held']:
            payment.status = 'refunded'
            payment.save()
            payment.client.account_balance += payment.amount
            payment.client.save()
            self.message_user(request, f'Payment {payment_id} refunded.')
        return redirect('admin:users_payment_changelist')
    
    from .models import HomepageSettings, ServiceCard, Testimonial, HomepageImage

@admin.register(HomepageSettings)
class HomepageSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Hero Section', {
            'fields': ('hero_title', 'hero_subtitle', 'hero_background_image', 'hero_background_color')
        }),
        ('Statistics Section', {
            'fields': ('stats_visible', 'stats_background_color')
        }),
        ('Services Section', {
            'fields': ('services_title', 'services_subtitle', 'services_visible')
        }),
        ('How It Works Section', {
            'fields': ('how_it_works_title', 'how_it_works_visible')
        }),
        ('Testimonials Section', {
            'fields': ('testimonials_title', 'testimonials_visible')
        }),
        ('Call to Action Section', {
            'fields': ('cta_title', 'cta_subtitle', 'cta_button1_text', 'cta_button2_text', 'cta_visible')
        }),
        ('Footer', {
            'fields': ('footer_copyright', 'footer_email', 'footer_phone')
        }),
        ('SEO', {
            'fields': ('meta_description', 'meta_keywords')
        }),
    )
    
    def has_add_permission(self, request):
        # Only allow one instance
        if HomepageSettings.objects.exists():
            return False
        return True


@admin.register(ServiceCard)
class ServiceCardAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)
    ordering = ('order',)


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'author_location', 'rating', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    list_filter = ('is_active', 'rating')


@admin.register(HomepageImage)
class HomepageImageAdmin(admin.ModelAdmin):
    list_display = ('section', 'image', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('section', 'is_active')


