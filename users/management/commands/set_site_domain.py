from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
import os

class Command(BaseCommand):
    help = 'Set the site domain dynamically'

    def handle(self, *args, **options):
        domain = os.environ.get('RAILWAY_PUBLIC_DOMAIN', 'buildimity.com')
        
        site, created = Site.objects.get_or_create(id=1)
        site.domain = domain
        site.name = 'Buidimty'
        site.save()
        
        self.stdout.write(self.style.SUCCESS(f'Site domain set to: {domain}'))