from django.core.management.base import BaseCommand
from users.models import IPWhitelistConfig
from users.ip_whitelist import IP_WHITELIST_CONFIG

class Command(BaseCommand):
    help = 'Sync IP whitelist configuration'

    def handle(self, *args, **options):
        # Sync MTN IPs
        for env in ['sandbox', 'production']:
            for ip in IP_WHITELIST_CONFIG['mtn'][env]:
                obj, created = IPWhitelistConfig.objects.get_or_create(
                    service='mtn',
                    environment=env,
                    ip_address=ip,
                    defaults={'description': f'MTN {env} server'}
                )
                if created:
                    self.stdout.write(f"Added MTN {env} IP: {ip}")
        
        # Sync Airtel IPs
        for env in ['sandbox', 'production']:
            for ip in IP_WHITELIST_CONFIG['airtel'][env]:
                obj, created = IPWhitelistConfig.objects.get_or_create(
                    service='airtel',
                    environment=env,
                    ip_address=ip,
                    defaults={'description': f'Airtel {env} server'}
                )
                if created:
                    self.stdout.write(f"Added Airtel {env} IP: {ip}")
        
        self.stdout.write(self.style.SUCCESS('IP whitelist sync complete!'))