from django.contrib import admin
from .models import Job, ServiceRequest


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'assigned_provider', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('client__username', 'assigned_provider__username', 'description')
