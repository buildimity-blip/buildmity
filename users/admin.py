from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, ProviderSearch

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_staff', 'date_joined')
    list_filter = ('role', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email', 'first_name', 'last_name')

@admin.register(ProviderSearch)
class ProviderSearchAdmin(admin.ModelAdmin):
    list_display = ('client', 'query', 'created_at')
    search_fields = ('client__username', 'query')
    list_filter = ('created_at',)