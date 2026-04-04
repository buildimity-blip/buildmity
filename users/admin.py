from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

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
            )
        }),
    )


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')
    ordering = ('name',)


@admin.register(ProviderWorkImage)
class ProviderWorkImageAdmin(admin.ModelAdmin):
    list_display = ('provider', 'caption', 'uploaded_at')
    search_fields = ('provider__username', 'caption')
    list_filter = ('uploaded_at',)
    ordering = ('-uploaded_at',)


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


@admin.register(ClientServiceNeed)
class ClientServiceNeedAdmin(admin.ModelAdmin):
    list_display = (
        'client',
        'service',
        'custom_service_name',
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


@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = (
        'client',
        'provider',
        'service',
        'service_need',
        'status',
        'amount',
        'commission',
        'provider_amount',
        'client_confirmed',
        'provider_confirmed',
        'created_at',
    )
    search_fields = (
        'client__username',
        'provider__username',
        'service__name',
        'message',
    )
    list_filter = ('status', 'service', 'created_at', 'accepted_at', 'completed_at')
    ordering = ('-created_at',)


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


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'service_request',
        'client',
        'provider',
        'method',
        'payer_phone_number',
        'amount',
        'commission',
        'provider_amount',
        'status',
        'transaction_id',
        'created_at',
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