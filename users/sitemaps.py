from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.contrib.sites.models import Site
from .models import Service, User


class StaticViewSitemap(Sitemap):
    """Sitemap for static pages"""
    priority = 0.8
    changefreq = 'daily'
    
    def items(self):
        return ['home', 'client_search', 'all_services']
    
    def location(self, item):
        return reverse(item)
    
    def protocol(self):
        return 'https' if not Site.objects.get_current().domain.startswith('localhost') else 'http'


class ServiceSitemap(Sitemap):
    """Sitemap for service pages"""
    priority = 0.9
    changefreq = 'weekly'
    
    def items(self):
        return Service.objects.filter(is_active=True).order_by('id')
    
    def lastmod(self, obj):
        return obj.created_at.date()
    
    def location(self, obj):
        return f'/services/{obj.id}/'


class ProviderSitemap(Sitemap):
    """Sitemap for provider profile pages"""
    priority = 0.7
    changefreq = 'weekly'
    
    def items(self):
        return User.objects.filter(
            role='provider', 
            is_verified=True, 
            is_active=True
        ).order_by('-date_joined')
    
    def lastmod(self, obj):
        return obj.date_joined.date()
    
    def location(self, obj):
        return f'/provider/{obj.id}/'