from decimal import Decimal
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login, authenticate, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.db import models
from django.db.models import Count, Q, Sum, Avg
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.http import HttpResponse

from .forms import (
    ClientSignUpForm, 
    ProviderSignupForm, 
    ProviderWorkImageForm,
    ClientSearchForm,
    RatingForm
)
from .models import (
    AdminNotification,
    ClientServiceNeed,
    ProviderSearch,
    ProviderWorkImage,
    Service,
    ServiceRequest,
    User,
    Negotiation,
    Payment,
    Rating,
    JobCompletion,
)


# ==================== HOME & ROBOTS ====================

def robots_txt(request):
    return HttpResponse(
        "User-agent: *\nAllow: /\nSitemap: https://buildimity.com/sitemap.xml",
        content_type="text/plain"
    )


def home(request):
    """Homepage view with dynamic content from admin"""
    from .models import HomepageSettings, ServiceCard, Testimonial, HomepageImage
    
    # Get homepage settings
    try:
        settings = HomepageSettings.objects.first()
    except:
        settings = None
    
    # Get service cards
    service_cards = ServiceCard.objects.filter(is_active=True)
    
    # Get testimonials
    testimonials = Testimonial.objects.filter(is_active=True)
    
    # Get hero background
    hero_image = HomepageImage.objects.filter(section='hero', is_active=True).first()
    
    # Get statistics
    total_providers = User.objects.filter(role='provider', is_verified=True).count()
    total_clients = User.objects.filter(role='client').count()
    total_services = Service.objects.filter(is_active=True).count()
    completed_jobs = ServiceRequest.objects.filter(status='completed').count()
    
    context = {
        # Settings
        'settings': settings,
        'hero_image': hero_image,
        'service_cards': service_cards,
        'testimonials': testimonials,
        
        # Statistics
        'total_providers': total_providers,
        'total_clients': total_clients,
        'total_services': total_services,
        'completed_jobs': completed_jobs,
        
        # Defaults if settings not configured
        'hero_title': settings.hero_title if settings else 'Find Trusted Service Providers Near You',
        'hero_subtitle': settings.hero_subtitle if settings else 'Connect with verified professionals...',
        'services_title': settings.services_title if settings else 'Popular Services',
        'how_it_works_title': settings.how_it_works_title if settings else 'How It Works',
        'testimonials_title': settings.testimonials_title if settings else 'What Our Customers Say',
        'cta_title': settings.cta_title if settings else 'Ready to Get Started?',
        'cta_subtitle': settings.cta_subtitle if settings else 'Join thousands of satisfied customers',
    }
    
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    return render(request, 'home.html', context)

# ==================== AUTHENTICATION & SIGNUP ====================

def signup_client(request):
    if request.method == 'POST':
        form = ClientSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect_after_login(request)
    else:
        form = ClientSignUpForm()
    return render(request, 'signup_client.html', {'form': form})


def signup_provider(request):
    """Provider registration - can select existing service or add new one"""
    if request.method == 'POST':
        form = ProviderSignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, f'Welcome! You are now registered as a provider.')
            return redirect('dashboard')
    else:
        form = ProviderSignupForm()
    return render(request, 'signup_provider.html', {'form': form})


def login_view(request):
    """Custom login view"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('redirect_after_login')
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
    return render(request, 'login.html')


def logout_view(request):
    auth_logout(request)
    return redirect('/')


def redirect_after_login(request):
    if getattr(request.user, 'is_suspended', False):
        return render(request, 'account_suspended.html')
    if request.user.is_staff or request.user.role == User.ADMIN:
        return redirect('admin_dashboard')
    return redirect('dashboard')


# ==================== CLIENT SEARCH & SERVICE REQUESTS ====================

def client_search(request):
    """Client searches for services and providers"""
    services = Service.objects.filter(is_active=True)
    providers = None
    search_performed = False
    query = request.GET.get('q', '')
    
    if query:
        search_performed = True
        providers = User.objects.filter(
            role='provider',
            is_active=True,
            is_suspended=False,
            is_verified=True,
            service__name__icontains=query
        ).select_related('service')
        
        if request.user.is_authenticated:
            ProviderSearch.objects.create(client=request.user, query=query)
        
        if not providers:
            messages.info(request, f'No providers found for "{query}". Try a different service.')
    
    context = {
        'services': services,
        'providers': providers,
        'search_performed': search_performed,
        'query': query,
    }
    return render(request, 'client_search.html', context)


def search_providers(request):
    """Search providers by query or service"""
    query = request.GET.get('q', '').strip()
    service_id = request.GET.get('service')
    providers = User.objects.none()
    services = Service.objects.filter(is_active=True).order_by('name')

    if query:
        if request.user.is_authenticated:
            ProviderSearch.objects.create(client=request.user, query=query)
        providers = User.objects.filter(
            role=User.PROVIDER,
            is_verified=True,
            is_suspended=False,
            is_active=True,
        ).filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(location__icontains=query) |
            Q(service__name__icontains=query)
        ).distinct()
    elif service_id:
        if request.user.is_authenticated:
            ProviderSearch.objects.create(client=request.user, query=f'service:{service_id}')
        providers = User.objects.filter(
            role=User.PROVIDER,
            is_verified=True,
            is_suspended=False,
            is_active=True,
            service_id=service_id,
        )

    return render(request, 'search_providers.html', {
        'providers': providers,
        'query': query,
        'services': services,
        'selected_service': service_id,
    })


def all_services(request):
    """View all available services with provider counts"""
    services = Service.objects.filter(is_active=True).annotate(
        provider_count=Count('providers', filter=Q(providers__role='provider', providers__is_active=True))
    )
    return render(request, 'all_services.html', {'services': services})


# ==================== DASHBOARD ====================

@login_required
def dashboard(request):
    if getattr(request.user, 'is_suspended', False):
        return render(request, 'account_suspended.html')

    if request.user.is_staff or request.user.role == User.ADMIN:
        return redirect('admin_dashboard')

    # PROVIDER DASHBOARD
    if request.user.role == User.PROVIDER:
        requests = ServiceRequest.objects.filter(
            provider=request.user
        ).select_related('client', 'service', 'service_need').order_by('-created_at')[:10]

        work_images = request.user.work_images.all().order_by('-uploaded_at')[:8]

        total_requests = ServiceRequest.objects.filter(provider=request.user).count()
        pending_requests = ServiceRequest.objects.filter(
            provider=request.user, status=ServiceRequest.PENDING
        ).count()
        accepted_requests = ServiceRequest.objects.filter(
            provider=request.user, status=ServiceRequest.ACCEPTED
        ).count()
        negotiating_requests = ServiceRequest.objects.filter(
            provider=request.user, status=ServiceRequest.NEGOTIATING
        ).count()
        completed_requests = ServiceRequest.objects.filter(
            provider=request.user, status=ServiceRequest.COMPLETED
        ).count()

        total_earnings = ServiceRequest.objects.filter(
            provider=request.user, status=ServiceRequest.COMPLETED
        ).aggregate(total=Sum('provider_amount'))['total'] or Decimal('0')

        context = {
            'user': request.user,
            'requests': requests,
            'work_images': work_images,
            'total_requests': total_requests,
            'pending_requests': pending_requests,
            'accepted_requests': accepted_requests,
            'negotiating_requests': negotiating_requests,
            'completed_requests': completed_requests,
            'total_earnings': total_earnings,
        }
        return render(request, 'dashboard.html', context)

    # CLIENT DASHBOARD
    needs = ClientServiceNeed.objects.filter(
        client=request.user
    ).select_related('service').order_by('-created_at')[:10]

    requests = ServiceRequest.objects.filter(
        client=request.user
    ).select_related('provider', 'service', 'service_need').order_by('-created_at')[:10]

    total_requests = ServiceRequest.objects.filter(client=request.user).count()
    pending_requests = ServiceRequest.objects.filter(
        client=request.user, status=ServiceRequest.PENDING
    ).count()
    accepted_requests = ServiceRequest.objects.filter(
        client=request.user, status=ServiceRequest.ACCEPTED
    ).count()
    negotiating_requests = ServiceRequest.objects.filter(
        client=request.user, status=ServiceRequest.NEGOTIATING
    ).count()
    completed_requests = ServiceRequest.objects.filter(
        client=request.user, status=ServiceRequest.COMPLETED
    ).count()

    recent_searches = ProviderSearch.objects.filter(
        client=request.user
    ).order_by('-created_at')[:5]

    context = {
        'user': request.user,
        'needs': needs,
        'requests': requests,
        'total_requests': total_requests,
        'pending_requests': pending_requests,
        'accepted_requests': accepted_requests,
        'negotiating_requests': negotiating_requests,
        'completed_requests': completed_requests,
        'services': Service.objects.filter(is_active=True).order_by('name'),
        'recent_searches': recent_searches,
    }
    return render(request, 'dashboard.html', context)


# ==================== SERVICE NEEDS ====================

@login_required
def create_service_need(request):
    if getattr(request.user, 'is_suspended', False):
        return render(request, 'account_suspended.html')

    if request.user.role != User.CLIENT:
        return redirect('dashboard')

    services = Service.objects.filter(is_active=True).order_by('name')

    if request.method == 'POST':
        service_id = request.POST.get('service')
        custom_service_name = request.POST.get('custom_service_name', '').strip()
        description = request.POST.get('description', '').strip()
        budget = request.POST.get('budget')
        location = request.POST.get('location', '').strip()
        preferred_date = request.POST.get('preferred_date')

        service = None
        if service_id:
            service = Service.objects.filter(id=service_id, is_active=True).first()

        budget_value = None
        if budget:
            try:
                budget_value = Decimal(str(budget))
            except Exception:
                budget_value = None

        need = ClientServiceNeed.objects.create(
            client=request.user,
            service=service,
            custom_service_name=custom_service_name if not service else '',
            description=description,
            budget=budget_value,
            location=location,
            preferred_date=preferred_date or None,
        )

        if need.is_unlisted_service():
            AdminNotification.objects.create(
                title='New unlisted service request',
                message=f"{request.user.username} requested '{need.custom_service_name}'",
                notification_type=AdminNotification.UNLISTED_SERVICE,
                related_user=request.user,
            )
            need.admin_notified = True
            need.save()

        return redirect('match_providers', need_id=need.id)

    return render(request, 'create_service_need.html', {'services': services})


@login_required
def match_providers(request, need_id):
    if getattr(request.user, 'is_suspended', False):
        return render(request, 'account_suspended.html')

    if request.user.role != User.CLIENT:
        return redirect('dashboard')

    need = get_object_or_404(ClientServiceNeed, id=need_id, client=request.user)

    providers = User.objects.filter(
        role=User.PROVIDER,
        is_verified=True,
        is_suspended=False,
        is_active=True,
    )

    if need.service:
        providers = providers.filter(service=need.service)
    elif need.custom_service_name:
        providers = providers.filter(service__name__icontains=need.custom_service_name)

    client_location = need.location or request.user.location
    
    if client_location:
        exact_location_providers = providers.filter(location__iexact=client_location)
        partial_location_providers = providers.filter(
            location__icontains=client_location
        ).exclude(id__in=exact_location_providers)
        other_providers = providers.exclude(
            id__in=exact_location_providers
        ).exclude(id__in=partial_location_providers)
        
        providers = list(exact_location_providers) + list(partial_location_providers) + list(other_providers)
    else:
        providers = providers.order_by('-is_verified', '-date_joined')

    if providers:
        need.status = ClientServiceNeed.MATCHED
        need.save()

    context = {
        'need': need,
        'providers': providers,
        'client_location': client_location,
    }
    return render(request, 'match_providers.html', context)


# ==================== SERVICE REQUESTS ====================

@login_required
def request_service(request, provider_id, need_id=None):
    if getattr(request.user, 'is_suspended', False):
        return render(request, 'account_suspended.html')

    if request.user.role != User.CLIENT:
        return redirect('dashboard')

    if need_id is None:
        need_id = request.GET.get('need_id')

    provider = get_object_or_404(
        User,
        id=provider_id,
        role=User.PROVIDER,
        is_verified=True,
        is_suspended=False,
        is_active=True,
    )

    need = None
    if need_id:
        try:
            need = get_object_or_404(ClientServiceNeed, id=need_id, client=request.user)
        except (ValueError, TypeError):
            pass

    if request.method == 'POST':
        message = request.POST.get('message', '').strip()
        amount = request.POST.get('amount', 0)

        try:
            amount = Decimal(str(amount))
        except Exception:
            amount = Decimal('0')

        service_request = ServiceRequest.objects.create(
            client=request.user,
            provider=provider,
            service_need=need,
            service=provider.service or (need.service if need else None),
            message=message,
            amount=amount,
            status=ServiceRequest.NEGOTIATING if amount > 0 else ServiceRequest.PENDING,
        )

        if need:
            need.status = ClientServiceNeed.NEGOTIATING
            need.save()

        messages.success(request, f'Request sent to {provider.username}.')
        return redirect('client_requests')

    context = {
        'provider': provider,
        'need': need,
    }
    return render(request, 'request_service.html', context)


@login_required
def service_request_detail(request, request_id):
    service_request = get_object_or_404(
        ServiceRequest.objects.select_related('client', 'provider', 'service', 'service_need'),
        id=request_id
    )

    if request.user not in [service_request.client, service_request.provider] and not request.user.is_staff:
        return redirect('dashboard')

    return render(request, 'service_request_detail.html', {
        'service_request': service_request,
        'negotiations': service_request.negotiations.select_related('sender').all(),
        'payment': getattr(service_request, 'payment', None),
    })


@login_required
def client_requests(request):
    if getattr(request.user, 'is_suspended', False):
        return render(request, 'account_suspended.html')

    requests = ServiceRequest.objects.filter(
        client=request.user
    ).select_related('provider', 'service', 'service_need').order_by('-created_at')

    return render(request, 'client_requests.html', {'requests': requests})


@login_required
def provider_requests(request):
    if getattr(request.user, 'is_suspended', False):
        return render(request, 'account_suspended.html')

    if request.user.role != User.PROVIDER:
        return redirect('dashboard')

    requests = ServiceRequest.objects.filter(
        provider=request.user
    ).select_related('client', 'service', 'service_need').order_by('-created_at')

    return render(request, 'provider_requests.html', {'requests': requests})

@login_required
def update_request_status(request, request_id, status):
    if getattr(request.user, 'is_suspended', False):
        return render(request, 'account_suspended.html')

    if request.user.role != User.PROVIDER:
        return redirect('dashboard')

    service_request = get_object_or_404(
        ServiceRequest,
        id=request_id,
        provider=request.user
    )

    if status == 'accepted':
        service_request.status = ServiceRequest.ACCEPTED
        service_request.accepted_at = timezone.now()
        messages.success(request, 'You have accepted the job. Waiting for client to make payment.')
        
    elif status == 'rejected':
        service_request.status = ServiceRequest.REJECTED
        messages.warning(request, 'You have rejected the job.')
        
    elif status == 'in_progress':
        service_request.status = ServiceRequest.IN_PROGRESS
        messages.success(request, 'You have started working on the job.')
        
    elif status == 'completed':
        service_request.status = ServiceRequest.COMPLETED
        service_request.completed_at = timezone.now()
        service_request.provider_confirmed = True
        messages.success(request, 'Job marked as completed. Waiting for client confirmation.')

    service_request.save()

    if service_request.service_need:
        if service_request.status == ServiceRequest.ACCEPTED:
            service_request.service_need.status = ClientServiceNeed.AGREED
        elif service_request.status == ServiceRequest.COMPLETED:
            service_request.service_need.status = ClientServiceNeed.COMPLETED
        elif service_request.status == ServiceRequest.REJECTED:
            service_request.service_need.status = ClientServiceNeed.CANCELLED
        elif service_request.status == ServiceRequest.IN_PROGRESS:
            service_request.service_need.status = ClientServiceNeed.IN_PROGRESS
        service_request.service_need.save()

    return redirect('provider_requests')


# ==================== NEGOTIATIONS ====================

@login_required
def negotiation_room(request, request_id):
    service_request = get_object_or_404(
        ServiceRequest.objects.select_related('client', 'provider', 'service', 'service_need'),
        id=request_id
    )

    if request.user not in [service_request.client, service_request.provider]:
        return redirect('dashboard')

    if request.method == 'POST':
        message_text = request.POST.get('message', '').strip()
        price_text = request.POST.get('price', '').strip()

        proposed_price = None
        if price_text:
            try:
                proposed_price = Decimal(price_text)
            except Exception:
                proposed_price = None

        if message_text or proposed_price is not None:
            Negotiation.objects.create(
                service_request=service_request,
                sender=request.user,
                message=message_text,
                proposed_price=proposed_price,
            )

            if proposed_price is not None:
                service_request.amount = proposed_price
                service_request.status = ServiceRequest.NEGOTIATING
                service_request.save()

            messages.success(request, 'Negotiation sent.')
            return redirect('negotiation_room', request_id=service_request.id)

    return render(request, 'negotiation_room.html', {
        'service_request': service_request,
        'negotiations': service_request.negotiations.select_related('sender').all(),
    })


# ==================== PAYMENTS ====================

@login_required
def make_payment(request, request_id):
    service_request = get_object_or_404(
        ServiceRequest.objects.select_related('client', 'provider'),
        id=request_id,
        client=request.user
    )

    if request.method == 'POST':
        method = request.POST.get('method')
        phone = request.POST.get('phone')
        amount_text = request.POST.get('amount')

        try:
            amount = Decimal(amount_text)
        except Exception:
            messages.error(request, 'Invalid amount.')
            return redirect('make_payment', request_id=request_id)

        payment, created = Payment.objects.get_or_create(
            service_request=service_request,
            defaults={
                'client': request.user,
                'provider': service_request.provider,
                'method': method,
                'payer_phone_number': phone,
                'amount': amount,
                'status': Payment.PAID,
                'paid_at': timezone.now(),
                'transaction_id': f"SIM-{timezone.now().strftime('%Y%m%d%H%M%S')}",
                'external_reference': f"REQ-{service_request.id}",
            }
        )

        if not created:
            payment.method = method
            payment.payer_phone_number = phone
            payment.amount = amount
            payment.status = Payment.PAID
            payment.paid_at = timezone.now()
            payment.transaction_id = f"SIM-{timezone.now().strftime('%Y%m%d%H%M%S')}"
            payment.save()

        service_request.amount = amount
        service_request.status = ServiceRequest.PAID
        service_request.save()

        if service_request.service_need:
            service_request.service_need.status = service_request.service_need.PAID
            service_request.service_need.save()

        messages.success(request, 'Payment recorded successfully.')
        return redirect('service_request_detail', request_id=request_id)

    return render(request, 'make_payment.html', {
        'service_request': service_request
    })


@login_required
def release_payment(request, request_id):
    service_request = get_object_or_404(
        ServiceRequest.objects.select_related('client', 'provider'),
        id=request_id,
        client=request.user
    )

    payment = getattr(service_request, 'payment', None)
    if not payment:
        messages.error(request, 'No payment found for this request.')
        return redirect('service_request_detail', request_id=request_id)

    if payment.status != Payment.PAID:
        messages.error(request, 'Payment is not ready for release.')
        return redirect('service_request_detail', request_id=request_id)

    payment.status = Payment.RELEASED
    payment.released_at = timezone.now()
    payment.save()

    provider = service_request.provider
    provider.account_balance += payment.provider_amount
    provider.save()

    service_request.status = ServiceRequest.COMPLETED
    service_request.completed_at = timezone.now()
    service_request.provider_confirmed = True
    service_request.client_confirmed = True
    service_request.save()

    if service_request.service_need:
        service_request.service_need.status = service_request.service_need.COMPLETED
        service_request.service_need.save()

    messages.success(request, 'Payment released to provider.')
    return redirect('service_request_detail', request_id=request_id)


# ==================== PROVIDER PROFILE ====================

@login_required
def provider_profile(request):
    if getattr(request.user, 'is_suspended', False):
        return render(request, 'account_suspended.html')

    if request.user.role != User.PROVIDER:
        return redirect('dashboard')

    if request.method == 'POST':
        request.user.first_name = request.POST.get('first_name', '').strip()
        request.user.last_name = request.POST.get('last_name', '').strip()
        request.user.email = request.POST.get('email', '').strip()
        request.user.phone_number = request.POST.get('phone_number', '').strip()
        request.user.location = request.POST.get('location', '').strip()
        request.user.bio = request.POST.get('bio', '').strip()
        request.user.preferred_payment_network = request.POST.get('preferred_payment_network', '').strip()
        request.user.mobile_money_number = request.POST.get('mobile_money_number', '').strip()

        if 'profile_photo' in request.FILES:
            request.user.profile_photo = request.FILES['profile_photo']

        request.user.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('provider_profile')

    return render(request, 'provider_profile.html', {
        'provider': request.user,
        'work_images': request.user.work_images.all().order_by('-uploaded_at')[:8],
    })


@login_required
def provider_detail(request, provider_id):
    if getattr(request.user, 'is_suspended', False):
        return render(request, 'account_suspended.html')

    provider = get_object_or_404(
        User,
        id=provider_id,
        role=User.PROVIDER,
        is_suspended=False,
        is_active=True,
    )

    work_images = provider.work_images.all().order_by('-uploaded_at')

    return render(request, 'provider_detail.html', {
        'provider': provider,
        'work_images': work_images,
    })


@login_required
def upload_work_image(request):
    if getattr(request.user, 'is_suspended', False):
        return render(request, 'account_suspended.html')

    if request.user.role != User.PROVIDER:
        return redirect('dashboard')

    if request.method == 'POST':
        form = ProviderWorkImageForm(request.POST, request.FILES)
        if form.is_valid():
            work_image = form.save(commit=False)
            work_image.provider = request.user
            work_image.save()
            messages.success(request, 'Work image uploaded successfully.')
            return redirect('dashboard')
    else:
        form = ProviderWorkImageForm()

    return render(request, 'upload_work_image.html', {'form': form})


# ==================== JOB COMPLETION & RATINGS ====================

@login_required
def confirm_completion(request, request_id):
    """Client confirms job completion"""
    service_request = get_object_or_404(ServiceRequest, id=request_id, client=request.user)
    
    if service_request.status != 'in_progress':
        messages.error(request, 'This request is not in progress.')
        return redirect('service_request_detail', request_id=request_id)
    
    if request.method == 'POST':
        service_request.status = 'completed'
        service_request.completed_at = timezone.now()
        service_request.client_confirmed = True
        service_request.save()
        
        messages.success(request, 'Job marked as completed! You can now rate the provider.')
        return redirect('rate_provider', request_id=request_id)
    
    return render(request, 'confirm_completion.html', {'service_request': service_request})


@login_required
def rate_provider(request, request_id):
    """Client rates the provider after job completion"""
    service_request = get_object_or_404(ServiceRequest, id=request_id, client=request.user)
    
    if hasattr(service_request, 'rating'):
        messages.info(request, 'You have already rated this provider.')
        return redirect('service_request_detail', request_id=request_id)
    
    if service_request.status != 'completed':
        messages.error(request, 'You can only rate after the job is completed.')
        return redirect('service_request_detail', request_id=request_id)
    
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.service_request = service_request
            rating.provider = service_request.provider
            rating.client = request.user
            rating.save()
            
            update_provider_rating(service_request.provider)
            
            messages.success(request, 'Thank you for rating! Your feedback helps other clients.')
            return redirect('service_request_detail', request_id=request_id)
    else:
        form = RatingForm()
    
    return render(request, 'rate_provider.html', {
        'service_request': service_request,
        'form': form
    })


@login_required
def provider_ratings(request, provider_id):
    """View all ratings for a provider"""
    provider = get_object_or_404(User, id=provider_id, role=User.PROVIDER)
    ratings = Rating.objects.filter(provider=provider, is_approved=True).select_related('client')
    
    avg_rating = ratings.aggregate(avg=Avg('rating'))['avg'] or 0
    
    distribution = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    for rating in ratings:
        distribution[rating.rating] += 1
    
    context = {
        'provider': provider,
        'ratings': ratings,
        'avg_rating': round(avg_rating, 1),
        'total_ratings': ratings.count(),
        'rating_distribution': distribution,
    }
    return render(request, 'provider_ratings.html', context)


@login_required
def provider_confirm_completion(request, request_id):
    """Provider confirms job completion"""
    service_request = get_object_or_404(ServiceRequest, id=request_id, provider=request.user)
    
    if request.method == 'POST':
        service_request.provider_confirmed = True
        service_request.status = 'in_progress'
        service_request.save()
        
        messages.success(request, 'You have confirmed completion. Waiting for client confirmation.')
        return redirect('provider_requests')
    
    return render(request, 'provider_confirm_completion.html', {'service_request': service_request})


def update_provider_rating(provider):
    """Calculate and update provider's average rating"""
    avg_rating = Rating.objects.filter(
        provider=provider,
        is_approved=True
    ).aggregate(avg=Avg('rating'))['avg'] or 0
    
    total_ratings = Rating.objects.filter(provider=provider, is_approved=True).count()
    
    provider.average_rating = round(avg_rating, 1)
    provider.total_ratings = total_ratings
    provider.save()
    
    return round(avg_rating, 1)


# ==================== PAYMENT POPUP VIEWS ====================

@login_required
def payment_popup(request, transaction_id):
    """Show payment popup/instructions page"""
    payment_data = request.session.get('payment_data', {})
    
    if not payment_data:
        messages.error(request, 'Payment session expired. Please try again.')
        return redirect('dashboard')
    
    context = {
        'transaction_id': transaction_id,
        'amount': payment_data.get('amount'),
        'phone_number': payment_data.get('phone_number'),
        'provider': payment_data.get('provider'),
        'ussd_code': payment_data.get('ussd_code'),
    }
    return render(request, 'payment_popup.html', context)


@login_required
def confirm_payment(request, transaction_id):
    """Confirm payment after user completes USSD transaction"""
    try:
        payment = Payment.objects.get(transaction_id=transaction_id)
        
        payment.status = 'paid'
        payment.paid_at = timezone.now()
        payment.save()
        
        service_request = payment.service_request
        service_request.status = 'paid'
        service_request.save()
        
        if service_request.service_need:
            service_request.service_need.status = 'paid'
            service_request.service_need.save()
        
        AdminNotification.objects.create(
            title='Payment Received',
            message=f'Payment of UGX {payment.amount} received from {payment.client.username} for request #{service_request.id}',
            notification_type='payment',
            related_user=payment.provider
        )
        
        if 'payment_data' in request.session:
            del request.session['payment_data']
        
        messages.success(request, 'Payment successful! The provider will start working on your request.')
        return redirect('service_request_detail', request_id=service_request.id)
        
    except Payment.DoesNotExist:
        messages.error(request, 'Payment not found.')
        return redirect('dashboard')


# ==================== ADMIN DASHBOARD ====================

@staff_member_required
def admin_dashboard(request):
    total_users = User.objects.count()
    total_clients = User.objects.filter(role=User.CLIENT).count()
    total_providers = User.objects.filter(role=User.PROVIDER).count()
    verified_providers = User.objects.filter(role=User.PROVIDER, is_verified=True).count()
    suspended_users = User.objects.filter(is_suspended=True).count()

    total_services = Service.objects.count()
    active_services = Service.objects.filter(is_active=True).count()

    total_searches = ProviderSearch.objects.count()
    total_requests = ServiceRequest.objects.count()
    pending_requests = ServiceRequest.objects.filter(status=ServiceRequest.PENDING).count()
    accepted_requests = ServiceRequest.objects.filter(status=ServiceRequest.ACCEPTED).count()
    rejected_requests = ServiceRequest.objects.filter(status=ServiceRequest.REJECTED).count()
    completed_requests = ServiceRequest.objects.filter(status=ServiceRequest.COMPLETED).count()

    total_work_images = ProviderWorkImage.objects.count()
    total_service_needs = ClientServiceNeed.objects.count()
    unlisted_service_needs = ClientServiceNeed.objects.filter(
        service__isnull=True
    ).exclude(custom_service_name='').count()
    unread_notifications = AdminNotification.objects.filter(is_read=False).count()

    total_revenue = ServiceRequest.objects.filter(
        status=ServiceRequest.COMPLETED
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0')

    total_commission = ServiceRequest.objects.filter(
        status=ServiceRequest.COMPLETED
    ).aggregate(total=Sum('commission'))['total'] or Decimal('0')

    top_services = Service.objects.annotate(
        provider_count=Count('providers'),
        request_count=Count('service_requests')
    ).order_by('-request_count', '-provider_count', 'name')[:5]

    most_searched_services = ProviderSearch.objects.values('query').annotate(
        total=Count('id')
    ).order_by('-total')[:5]

    top_providers = User.objects.filter(
        role=User.PROVIDER
    ).annotate(
        request_count=Count('received_service_requests'),
        completed_count=Count(
            'received_service_requests',
            filter=Q(received_service_requests__status=ServiceRequest.COMPLETED)
        ),
        rejected_count=Count(
            'received_service_requests',
            filter=Q(received_service_requests__status=ServiceRequest.REJECTED)
        ),
        total_earnings=Sum(
            'received_service_requests__provider_amount',
            filter=Q(received_service_requests__status=ServiceRequest.COMPLETED)
        ),
    ).order_by('-completed_count', '-total_earnings')[:5]

    recent_searches = ProviderSearch.objects.select_related('client').order_by('-created_at')[:10]
    recent_requests = ServiceRequest.objects.select_related('client', 'provider', 'service').order_by('-created_at')[:10]
    recent_providers = User.objects.filter(role=User.PROVIDER).order_by('-date_joined')[:10]
    recent_images = ProviderWorkImage.objects.select_related('provider').order_by('-uploaded_at')[:12]
    recent_needs = ClientServiceNeed.objects.select_related('client', 'service').order_by('-created_at')[:10]
    recent_notifications = AdminNotification.objects.select_related('related_user').order_by('-created_at')[:10]

    context = {
        'total_users': total_users,
        'total_clients': total_clients,
        'total_providers': total_providers,
        'verified_providers': verified_providers,
        'suspended_users': suspended_users,
        'total_services': total_services,
        'active_services': active_services,
        'total_searches': total_searches,
        'total_requests': total_requests,
        'pending_requests': pending_requests,
        'accepted_requests': accepted_requests,
        'rejected_requests': rejected_requests,
        'completed_requests': completed_requests,
        'total_work_images': total_work_images,
        'total_service_needs': total_service_needs,
        'unlisted_service_needs': unlisted_service_needs,
        'unread_notifications': unread_notifications,
        'total_revenue': total_revenue,
        'total_commission': total_commission,
        'top_services': top_services,
        'most_searched_services': most_searched_services,
        'top_providers': top_providers,
        'recent_searches': recent_searches,
        'recent_requests': recent_requests,
        'recent_providers': recent_providers,
        'recent_images': recent_images,
        'recent_needs': recent_needs,
        'recent_notifications': recent_notifications,
        'pending_providers': User.objects.filter(role='provider', is_verified=False)[:10],
        'pending_payments': Payment.objects.filter(status='held')[:10],
        'recent_users': User.objects.order_by('-date_joined')[:10],
        'storage_usage': 45,
        'active_sessions': 12,
        'today_visitors': 0,
    }

    return render(request, 'admin_dashboard.html', context)


@staff_member_required
def admin_user_detail(request, user_id):
    user_obj = get_object_or_404(User, id=user_id)

    requests_sent = ServiceRequest.objects.filter(
        client=user_obj
    ).select_related('provider', 'service').order_by('-created_at')[:10]

    requests_received = ServiceRequest.objects.filter(
        provider=user_obj
    ).select_related('client', 'service').order_by('-created_at')[:10]

    service_needs = ClientServiceNeed.objects.filter(
        client=user_obj
    ).select_related('service').order_by('-created_at')[:10]

    work_images = user_obj.work_images.all().order_by('-uploaded_at')[:8] if user_obj.role == User.PROVIDER else []

    context = {
        'user_obj': user_obj,
        'requests_sent': requests_sent,
        'requests_received': requests_received,
        'service_needs': service_needs,
        'work_images': work_images,
    }
    return render(request, 'admin_user_detail.html', context)


@staff_member_required
def approve_provider(request, user_id):
    user_obj = get_object_or_404(User, id=user_id, role=User.PROVIDER)
    user_obj.is_verified = True
    user_obj.is_suspended = False
    user_obj.is_active = True
    user_obj.save()

    messages.success(request, f'{user_obj.username} approved successfully.')
    return redirect('admin_dashboard')


@staff_member_required
def ignore_provider(request, user_id):
    user_obj = get_object_or_404(User, id=user_id, role=User.PROVIDER)
    messages.info(request, f'No changes made to {user_obj.username}.')
    return redirect('admin_dashboard')


@staff_member_required
def suspend_user(request, user_id):
    user_obj = get_object_or_404(User, id=user_id)
    user_obj.is_suspended = True
    user_obj.is_active = False
    user_obj.save()

    messages.warning(request, f'{user_obj.username} suspended.')
    return redirect('admin_dashboard')

# ==================== DISPUTE RESOLUTION ====================

@login_required
def raise_dispute(request, request_id):
    """Client or provider raises a dispute"""
    service_request = get_object_or_404(ServiceRequest, id=request_id)
    
    if request.user not in [service_request.client, service_request.provider]:
        messages.error(request, 'You cannot raise a dispute for this request.')
        return redirect('service_request_detail', request_id=request_id)
    
    # Check if dispute already exists
    if hasattr(service_request, 'dispute'):
        messages.warning(request, 'A dispute already exists for this request.')
        return redirect('dispute_detail', dispute_id=service_request.dispute.id)
    
    if request.method == 'POST':
        dispute = Dispute.objects.create(
            service_request=service_request,
            raised_by=request.user,
            reason=request.POST.get('reason'),
            description=request.POST.get('description'),
            evidence_images=request.FILES.get('evidence_images'),
            evidence_documents=request.FILES.get('evidence_documents'),
            status='open'
        )
        
        # Create admin notification
        AdminNotification.objects.create(
            title=f'New Dispute Raised',
            message=f'Dispute raised for request #{service_request.id} by {request.user.username}',
            notification_type='general',
            related_user=request.user
        )
        
        messages.success(request, 'Dispute raised successfully. Admin will review shortly.')
        return redirect('dispute_detail', dispute_id=dispute.id)
    
    return render(request, 'raise_dispute.html', {'service_request': service_request})


@login_required
def dispute_detail(request, dispute_id):
    """View dispute details and messages"""
    dispute = get_object_or_404(Dispute.objects.select_related('service_request', 'raised_by'), id=dispute_id)
    service_request = dispute.service_request
    
    # Check permission
    if request.user not in [service_request.client, service_request.provider] and not request.user.is_staff:
        messages.error(request, 'You do not have permission to view this dispute.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        message = request.POST.get('message')
        if message:
            DisputeMessage.objects.create(
                dispute=dispute,
                sender=request.user,
                message=message,
                is_admin_message=request.user.is_staff
            )
            messages.success(request, 'Message added to dispute.')
        
        # Admin resolution
        if request.user.is_staff and request.POST.get('resolve'):
            dispute.status = request.POST.get('status')
            dispute.resolution = request.POST.get('resolution')
            dispute.resolution_notes = request.POST.get('resolution_notes')
            dispute.resolved_by = request.user
            dispute.resolved_at = timezone.now()
            dispute.save()
            
            # Handle resolution actions
            if dispute.resolution == 'refund_client':
                payment = service_request.payment
                if payment:
                    payment.status = 'refunded'
                    payment.save()
                    service_request.client.account_balance += payment.amount
                    service_request.client.save()
            elif dispute.resolution == 'release_to_provider':
                payment = service_request.payment
                if payment:
                    payment.status = 'released'
                    payment.save()
                    service_request.provider.account_balance += payment.provider_amount
                    service_request.provider.save()
            
            messages.success(request, 'Dispute resolved successfully.')
        
        return redirect('dispute_detail', dispute_id=dispute.id)
    
    messages_list = dispute.messages.all().order_by('created_at')
    
    return render(request, 'dispute_detail.html', {
        'dispute': dispute,
        'service_request': service_request,
        'messages': messages_list,
        'is_admin': request.user.is_staff,
    })


@staff_member_required
def admin_disputes(request):
    """Admin panel for managing disputes"""
    disputes = Dispute.objects.select_related('service_request', 'raised_by').all()
    
    status_filter = request.GET.get('status', '')
    if status_filter:
        disputes = disputes.filter(status=status_filter)
    
    context = {
        'disputes': disputes,
        'status_choices': Dispute.STATUS_CHOICES,
        'open_count': disputes.filter(status='open').count(),
        'under_review_count': disputes.filter(status='under_review').count(),
        'resolved_count': disputes.filter(status='resolved').count(),
    }
    return render(request, 'admin_disputes.html', context)

# ==================== ADVANCED ANALYTICS ====================

from django.db.models.functions import TruncDate, TruncMonth, TruncWeek
from django.utils import timezone
from datetime import timedelta
import json

@staff_member_required
def analytics_dashboard(request):
    """Advanced analytics dashboard with charts"""
    
    # Date ranges
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    year_ago = today - timedelta(days=365)
    
    # Revenue data (last 30 days)
    revenue_data = []
    for i in range(30):
        date = today - timedelta(days=i)
        date_start = timezone.make_aware(timezone.datetime.combine(date, timezone.datetime.min.time()))
        date_end = timezone.make_aware(timezone.datetime.combine(date, timezone.datetime.max.time()))
        
        revenue = Payment.objects.filter(
            status='paid',
            paid_at__range=(date_start, date_end)
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        revenue_data.append({
            'date': date.strftime('%Y-%m-%d'),
            'revenue': float(revenue)
        })
    
    # User growth (last 12 months)
    user_growth = []
    for i in range(12):
        month = today.replace(day=1) - timedelta(days=30 * i)
        month_start = timezone.make_aware(timezone.datetime.combine(month.replace(day=1), timezone.datetime.min.time()))
        next_month = month.replace(day=28) + timedelta(days=4)
        month_end = timezone.make_aware(timezone.datetime.combine(next_month - timedelta(days=next_month.day), timezone.datetime.max.time()))
        
        new_users = User.objects.filter(date_joined__range=(month_start, month_end)).count()
        user_growth.append({
            'month': month.strftime('%B %Y'),
            'users': new_users
        })
    
    # Request status distribution
    status_distribution = {
        'pending': ServiceRequest.objects.filter(status='pending').count(),
        'accepted': ServiceRequest.objects.filter(status='accepted').count(),
        'in_progress': ServiceRequest.objects.filter(status='in_progress').count(),
        'completed': ServiceRequest.objects.filter(status='completed').count(),
        'rejected': ServiceRequest.objects.filter(status='rejected').count(),
    }
    
    # Top services by revenue
    top_services_revenue = Service.objects.annotate(
        total_revenue=Sum('service_requests__amount', filter=Q(service_requests__status='completed'))
    ).order_by('-total_revenue')[:5]
    
    # Provider performance
    provider_performance = User.objects.filter(
        role='provider'
    ).annotate(
        total_jobs=Count('received_service_requests', filter=Q(received_service_requests__status='completed')),
        total_earnings=Sum('received_service_requests__provider_amount', filter=Q(received_service_requests__status='completed')),
        avg_rating=Avg('received_ratings__rating')
    ).order_by('-total_jobs')[:10]
    
    # Geographic distribution (if location data available)
    locations = User.objects.filter(role='client').values('location').annotate(count=Count('id')).order_by('-count')[:10]
    
    context = {
        'revenue_data': json.dumps(revenue_data),
        'user_growth': json.dumps(user_growth[::-1]),  # Reverse for chronological order
        'status_distribution': json.dumps(status_distribution),
        'top_services_revenue': top_services_revenue,
        'provider_performance': provider_performance,
        'locations': locations,
        'total_revenue': Payment.objects.filter(status='paid').aggregate(total=Sum('amount'))['total'] or 0,
        'total_commission': Payment.objects.filter(status='paid').aggregate(total=Sum('commission'))['total'] or 0,
        'total_users': User.objects.count(),
        'active_providers': User.objects.filter(role='provider', is_verified=True, is_active=True).count(),
        'completion_rate': (ServiceRequest.objects.filter(status='completed').count() / ServiceRequest.objects.count() * 100) if ServiceRequest.objects.count() > 0 else 0,
    }
    
    return render(request, 'analytics_dashboard.html', context)


@staff_member_required
def export_report(request, report_type):
    """Export reports as CSV/Excel"""
    import csv
    from django.http import HttpResponse
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{report_type}_report_{timezone.now().date()}.csv"'
    
    writer = csv.writer(response)
    
    if report_type == 'users':
        writer.writerow(['Username', 'Email', 'Role', 'Joined Date', 'Verified', 'Suspended'])
        users = User.objects.all()
        for user in users:
            writer.writerow([user.username, user.email, user.role, user.date_joined, user.is_verified, user.is_suspended])
    
    elif report_type == 'payments':
        writer.writerow(['Request ID', 'Client', 'Provider', 'Amount', 'Commission', 'Status', 'Date'])
        payments = Payment.objects.select_related('client', 'provider', 'service_request')
        for payment in payments:
            writer.writerow([
                payment.service_request.id, payment.client.username, payment.provider.username,
                payment.amount, payment.commission, payment.status, payment.paid_at
            ])
    
    elif report_type == 'requests':
        writer.writerow(['Request ID', 'Client', 'Provider', 'Service', 'Amount', 'Status', 'Created'])
        requests = ServiceRequest.objects.select_related('client', 'provider', 'service')
        for req in requests:
            writer.writerow([
                req.id, req.client.username, req.provider.username,
                req.service.name if req.service else 'N/A',
                req.amount, req.status, req.created_at
            ])
    
    return response

# ==================== MOBILE APP API ====================

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, ServiceSerializer, ServiceRequestSerializer, PaymentSerializer, RatingSerializer

@api_view(['GET'])
def api_home(request):
    """API home endpoint"""
    return Response({
        'message': 'Buildimity API v1',
        'endpoints': {
            'auth': '/api/login/',
            'register': '/api/register/',
            'services': '/api/services/',
            'requests': '/api/my-requests/',
            'profile': '/api/profile/',
            'providers': '/api/providers/',
        }
    })


@api_view(['POST'])
def api_register(request):
    """User registration via API"""
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    role = request.data.get('role', 'client')
    
    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        role=role
    )
    
    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_profile(request):
    """Get user profile"""
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_services(request):
    """List all services"""
    services = Service.objects.filter(is_active=True)
    serializer = ServiceSerializer(services, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_providers(request):
    """List providers with optional service filter"""
    service_id = request.GET.get('service')
    providers = User.objects.filter(role='provider', is_verified=True, is_active=True)
    
    if service_id:
        providers = providers.filter(service_id=service_id)
    
    serializer = UserSerializer(providers, many=True)
    return Response(serializer.data)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def api_my_requests(request):
    """Get or create service requests"""
    if request.method == 'GET':
        requests = ServiceRequest.objects.filter(client=request.user).order_by('-created_at')
        serializer = ServiceRequestSerializer(requests, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        provider_id = request.data.get('provider_id')
        message = request.data.get('message')
        amount = request.data.get('amount', 0)
        
        provider = get_object_or_404(User, id=provider_id, role='provider')
        
        service_request = ServiceRequest.objects.create(
            client=request.user,
            provider=provider,
            message=message,
            amount=amount,
            status='pending'
        )
        
        serializer = ServiceRequestSerializer(service_request)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_make_payment(request, request_id):
    """Initiate payment via API"""
    service_request = get_object_or_404(ServiceRequest, id=request_id, client=request.user)
    
    method = request.data.get('method')
    phone_number = request.data.get('phone_number')
    
    # Mock payment processing
    payment = Payment.objects.create(
        service_request=service_request,
        client=request.user,
        provider=service_request.provider,
        method=method,
        payer_phone_number=phone_number,
        amount=service_request.amount,
        commission=service_request.amount * Decimal('0.10'),
        provider_amount=service_request.amount * Decimal('0.90'),
        status='pending',
        transaction_id=f"API-{timezone.now().timestamp()}"
    )
    
    serializer = PaymentSerializer(payment)
    return Response(serializer.data)
@login_required
def service_checklist(request, request_id):
    """Manage service completion checklist"""
    service_request = get_object_or_404(ServiceRequest, id=request_id)
    
    if request.user not in [service_request.client, service_request.provider]:
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    # Create default checklist items if none exist
    if service_request.checklist_items.count() == 0:
        default_items = [
            'Service completed as agreed',
            'Quality meets expectations',
            'All issues resolved',
            'Client satisfied with work',
            'Payment confirmed',
        ]
        for item in default_items:
            ServiceChecklist.objects.create(
                service_request=service_request,
                item_name=item
            )
    
    if request.method == 'POST':
        # Update checklist items
        for item in service_request.checklist_items.all():
            checked = request.POST.get(f'item_{item.id}') == 'on'
            if checked and not item.is_completed:
                item.is_completed = True
                item.completed_by = request.user
                item.completed_at = timezone.now()
                item.save()
            elif not checked and item.is_completed:
                item.is_completed = False
                item.completed_by = None
                item.completed_at = None
                item.save()
        
        # Upload completion photo
        if request.FILES.get('completion_photo'):
            CompletionPhoto.objects.create(
                service_request=service_request,
                image=request.FILES['completion_photo'],
                caption=request.POST.get('photo_caption', ''),
                uploaded_by=request.user
            )
        
        messages.success(request, 'Checklist updated successfully.')
        return redirect('service_checklist', request_id=request_id)
    
    checklist_items = service_request.checklist_items.all()
    completion_photos = service_request.completion_photos.all()
    all_completed = all(item.is_completed for item in checklist_items)
    
    context = {
        'service_request': service_request,
        'checklist_items': checklist_items,
        'completion_photos': completion_photos,
        'all_completed': all_completed,
        'is_provider': request.user == service_request.provider,
        'is_client': request.user == service_request.client,
    }
    return render(request, 'service_checklist.html', context)

# ==================== MOBILE APP API ENHANCED ====================

from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.db.models import Q
from decimal import Decimal

@api_view(['POST'])
def api_login(request):
    """API login endpoint - returns token"""
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(request, username=username, password=password)
    
    if user:
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'is_verified': user.is_verified,
        })
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def api_logout(request):
    """API logout endpoint"""
    request.user.auth_token.delete()
    return Response({'message': 'Logged out successfully'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_notifications(request):
    """Get user notifications"""
    notifications = AdminNotification.objects.filter(
        related_user=request.user
    ).order_by('-created_at')[:20]
    
    data = [{
        'id': n.id,
        'title': n.title,
        'message': n.message,
        'is_read': n.is_read,
        'created_at': n.created_at.isoformat(),
    } for n in notifications]
    
    return Response(data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_mark_notification_read(request, notification_id):
    """Mark notification as read"""
    notification = get_object_or_404(AdminNotification, id=notification_id, related_user=request.user)
    notification.is_read = True
    notification.save()
    return Response({'message': 'Notification marked as read'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_search_providers(request):
    """Search providers with filters"""
    query = request.GET.get('q', '')
    service_id = request.GET.get('service_id')
    location = request.GET.get('location', '')
    min_rating = request.GET.get('min_rating', 0)
    
    providers = User.objects.filter(
        role='provider',
        is_verified=True,
        is_active=True,
        is_suspended=False
    )
    
    if query:
        providers = providers.filter(
            Q(username__icontains=query) |
            Q(service__name__icontains=query) |
            Q(location__icontains=query)
        )
    
    if service_id:
        providers = providers.filter(service_id=service_id)
    
    if location:
        providers = providers.filter(location__icontains=location)
    
    if min_rating:
        providers = providers.filter(average_rating__gte=min_rating)
    
    # Annotate with additional info
    providers = providers.annotate(
        job_count=Count('received_service_requests', filter=Q(received_service_requests__status='completed'))
    ).order_by('-average_rating', '-job_count')[:50]
    
    serializer = UserSerializer(providers, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_provider_detail(request, provider_id):
    """Get detailed provider info including work images and ratings"""
    provider = get_object_or_404(
        User, 
        id=provider_id, 
        role='provider',
        is_active=True
    )
    
    work_images = ProviderWorkImage.objects.filter(provider=provider).values('id', 'image', 'caption')
    ratings = Rating.objects.filter(provider=provider, is_approved=True).values('rating', 'review', 'created_at')
    
    # Calculate rating stats
    from django.db.models import Avg
    avg_rating = ratings.aggregate(avg=Avg('rating'))['avg'] or 0
    
    data = {
        'id': provider.id,
        'username': provider.username,
        'service': provider.service.name if provider.service else None,
        'location': provider.location,
        'phone_number': provider.phone_number,
        'bio': provider.bio,
        'profile_photo': provider.profile_photo.url if provider.profile_photo else None,
        'is_verified': provider.is_verified,
        'average_rating': float(avg_rating),
        'total_ratings': ratings.count(),
        'work_images': list(work_images),
        'recent_ratings': list(ratings.order_by('-created_at')[:5]),
    }
    
    return Response(data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_create_service_request(request):
    """Create a new service request from mobile app"""
    provider_id = request.data.get('provider_id')
    message = request.data.get('message', '')
    amount = request.data.get('amount', 0)
    service_need_id = request.data.get('service_need_id')
    
    provider = get_object_or_404(User, id=provider_id, role='provider')
    
    service_need = None
    if service_need_id:
        service_need = get_object_or_404(ClientServiceNeed, id=service_need_id, client=request.user)
    
    service_request = ServiceRequest.objects.create(
        client=request.user,
        provider=provider,
        service_need=service_need,
        service=provider.service,
        message=message,
        amount=Decimal(str(amount)),
        status='pending'
    )
    
    serializer = ServiceRequestSerializer(service_request)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_update_profile(request):
    """Update user profile from mobile app"""
    user = request.user
    
    user.first_name = request.data.get('first_name', user.first_name)
    user.last_name = request.data.get('last_name', user.last_name)
    user.phone_number = request.data.get('phone_number', user.phone_number)
    user.location = request.data.get('location', user.location)
    user.bio = request.data.get('bio', user.bio)
    
    if request.data.get('profile_photo'):
        # Handle base64 image upload
        import base64
        from django.core.files.base import ContentFile
        
        format, imgstr = request.data.get('profile_photo').split(';base64,')
        ext = format.split('/')[-1]
        data = ContentFile(base64.b64decode(imgstr), name=f'profile.{ext}')
        user.profile_photo = data
    
    user.save()
    
    serializer = UserSerializer(user)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_dashboard_stats(request):
    """Get dashboard statistics for mobile app"""
    if request.user.role == 'client':
        total_requests = ServiceRequest.objects.filter(client=request.user).count()
        pending_requests = ServiceRequest.objects.filter(client=request.user, status='pending').count()
        active_requests = ServiceRequest.objects.filter(
            client=request.user, 
            status__in=['accepted', 'in_progress', 'negotiating']
        ).count()
        completed_requests = ServiceRequest.objects.filter(client=request.user, status='completed').count()
        
        recent_requests = ServiceRequest.objects.filter(client=request.user).order_by('-created_at')[:5]
        
    else:  # provider
        total_requests = ServiceRequest.objects.filter(provider=request.user).count()
        pending_requests = ServiceRequest.objects.filter(provider=request.user, status='pending').count()
        active_requests = ServiceRequest.objects.filter(
            provider=request.user,
            status__in=['accepted', 'in_progress', 'negotiating']
        ).count()
        completed_requests = ServiceRequest.objects.filter(provider=request.user, status='completed').count()
        total_earnings = ServiceRequest.objects.filter(
            provider=request.user, 
            status='completed'
        ).aggregate(total=Sum('provider_amount'))['total'] or 0
        
        recent_requests = ServiceRequest.objects.filter(provider=request.user).order_by('-created_at')[:5]
    
    recent_data = ServiceRequestSerializer(recent_requests, many=True).data
    
    return Response({
        'total_requests': total_requests,
        'pending_requests': pending_requests,
        'active_requests': active_requests,
        'completed_requests': completed_requests,
        'total_earnings': float(total_earnings) if request.user.role == 'provider' else 0,
        'recent_requests': recent_data,
    })
@login_required
def my_referrals(request):
    """Simple placeholder for referrals"""
    return render(request, 'my_referrals.html', {
        'referral_code': request.user.username.upper(),
        'referral_link': request.build_absolute_uri('/signup/client/'),
        'sent_count': 0,
        'successful_count': 0,
        'total_earned': 0,
        'referrals': [],
    })
