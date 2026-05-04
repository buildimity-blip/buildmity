from django.core.management.base import BaseCommand
from users.models import HomepageSettings, ServiceCard, Testimonial, Service

class Command(BaseCommand):
    help = 'Initialize homepage settings'

    def handle(self, *args, **options):
        # Create homepage settings
        if not HomepageSettings.objects.exists():
            HomepageSettings.objects.create()
            self.stdout.write(self.style.SUCCESS('✓ Homepage settings created'))
        
        # Create default service cards if none exist
        if ServiceCard.objects.count() == 0:
            default_services = [
                ('Plumbing', 'fa-wrench', 'Pipe installation, repairs, and maintenance'),
                ('Electrical', 'fa-bolt', 'Wiring, installations, and electrical repairs'),
                ('Cleaning', 'fa-broom', 'Home and office cleaning services'),
                ('Painting', 'fa-paint-roller', 'Interior and exterior painting'),
                ('Carpentry', 'fa-hammer', 'Furniture making and repairs'),
                ('General Repairs', 'fa-tools', 'Home and appliance repairs'),
            ]
            
            for i, (name, icon, desc) in enumerate(default_services):
                ServiceCard.objects.create(
                    custom_name=name,
                    icon=icon,
                    description=desc,
                    order=i
                )
            self.stdout.write(self.style.SUCCESS(f'✓ Created {len(default_services)} service cards'))
        
        # Create default testimonials
        if Testimonial.objects.count() == 0:
            default_testimonials = [
                ('John M.', 'Kampala', 'Found a great plumber within hours. The platform is easy to use and the provider was professional.', 5),
                ('Sarah K.', 'Electrician', 'As a provider, I\'ve gotten many clients through this platform. Highly recommended!', 5),
                ('Michael O.', 'Ntinda', 'Secure payment and great support. Will definitely use again for all my home services.', 5),
            ]
            
            for i, (name, location, content, rating) in enumerate(default_testimonials):
                Testimonial.objects.create(
                    author_name=name,
                    author_location=location,
                    content=content,
                    rating=rating,
                    order=i
                )
            self.stdout.write(self.style.SUCCESS(f'✓ Created {len(default_testimonials)} testimonials'))
        
        self.stdout.write(self.style.SUCCESS('✅ Homepage initialization complete!'))