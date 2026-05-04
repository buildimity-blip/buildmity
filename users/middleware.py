# users/middleware.py
from django.contrib.sites.models import Site
from django.utils.deprecation import MiddlewareMixin

class DynamicSiteMiddleware(MiddlewareMixin):
    """
    Dynamically update the site domain based on the request host.
    This allows Google OAuth to work with multiple domains (Railway, buildimity.com, localhost).
    """
    def process_request(self, request):
        # Get the host from request
        host = request.get_host().split(':')[0]  # Remove port number
        
        # Skip for localhost to avoid unnecessary updates
        if host in ['localhost', '127.0.0.1']:
            return
        
        try:
            site = Site.objects.get_current()
            if site.domain != host:
                site.domain = host
                site.name = host
                site.save()
        except Exception:
            pass