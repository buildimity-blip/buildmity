from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .forms import ClientSignUpForm, ProviderSignUpForm, ProviderWorkImageForm
from .models import User, ProviderSearch, ProviderWorkImage
from jobs.models import ServiceRequest
from django.db import models

def signup_client(request):
    if request.method == 'POST':
        form = ClientSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = ClientSignUpForm()

    return render(request, 'signup_client.html', {'form': form})


def signup_provider(request):
    if request.method == 'POST':
        form = ProviderSignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = ProviderSignUpForm()

    return render(request, 'signup_provider.html', {'form': form})


@login_required
def search_providers(request):
    query = request.GET.get('q', '')
    providers = []

    if query:
        ProviderSearch.objects.create(
            client=request.user,
            query=query
        )

        providers = User.objects.filter(
            role='provider',
            username__icontains=query
        ) | User.objects.filter(
            role='provider',
            first_name__icontains=query
        ) | User.objects.filter(
            role='provider',
            last_name__icontains=query
        )

    return render(request, 'search_providers.html', {
        'providers': providers,
        'query': query
    })


@login_required
def provider_detail(request, provider_id):
    provider = get_object_or_404(User, id=provider_id, role='provider')
    return render(request, 'provider_detail.html', {'provider': provider})


@login_required
def request_service(request, provider_id):
    provider = get_object_or_404(User, id=provider_id, role='provider')

    if request.method == 'POST':
        message = request.POST.get('message', '')
        ServiceRequest.objects.create(
            client=request.user,
            provider=provider,
            message=message
        )
        return redirect('client_requests')

    return render(request, 'request_service.html', {'provider': provider})


@login_required
def client_requests(request):
    requests = ServiceRequest.objects.filter(client=request.user).order_by('-created_at')
    return render(request, 'client_requests.html', {'requests': requests})


@login_required
def provider_requests(request):
    requests = ServiceRequest.objects.filter(provider=request.user).order_by('-created_at')
    return render(request, 'provider_requests.html', {'requests': requests})


@login_required
def upload_work_image(request):
    if request.user.role != 'provider':
        return redirect('dashboard')

    if request.method == 'POST':
        form = ProviderWorkImageForm(request.POST, request.FILES)
        if form.is_valid():
            work = form.save(commit=False)
            work.provider = request.user
            work.save()
            return redirect('dashboard')
    else:
        form = ProviderWorkImageForm()

    return render(request, 'upload_work_image.html', {'form': form})

from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Sum
from django.shortcuts import render

from .models import User, ProviderSearch, ProviderWorkImage, Service
from jobs.models import ServiceRequest

from django.db.models import Count, Sum, Q

@staff_member_required
def admin_dashboard(request):
    total_clients = User.objects.filter(role='client').count()
    total_providers = User.objects.filter(role='provider').count()
    total_searches = ProviderSearch.objects.count()
    total_requests = ServiceRequest.objects.count()

    completed_jobs = ServiceRequest.objects.filter(status='completed').count()
    cancelled_jobs = ServiceRequest.objects.filter(status='cancelled').count()
    pending_requests = ServiceRequest.objects.filter(status='pending').count()

    total_work_images = ProviderWorkImage.objects.count()

    total_revenue = ServiceRequest.objects.filter(status='completed').aggregate(
        total=Sum('amount')
    )['total'] or 0

    total_commission = ServiceRequest.objects.filter(status='completed').aggregate(
        total=Sum('commission')
    )['total'] or 0

    # ✅ FIXED: use provider.service_name instead
    top_services = User.objects.filter(role='provider').values('service__name').annotate(
    total=Count('id')
).exclude(service__isnull=True).order_by('-total')[:5]

    most_searched_services = ProviderSearch.objects.values('query').annotate(
        total=Count('id')
    ).order_by('-total')[:5]

    # ✅ FIXED: correct related_name
    top_providers = User.objects.filter(role='provider').annotate(
        completed_count=Count(
            'provider_requests',
            filter=Q(provider_requests__status='completed')
        ),
        cancelled_count=Count(
            'provider_requests',
            filter=Q(provider_requests__status='cancelled')
        ),
        total_earnings=Sum(
            'provider_requests__amount',
            filter=Q(provider_requests__status='completed')
        )
    ).order_by('-completed_count', '-total_earnings')[:5]

    recent_searches = ProviderSearch.objects.order_by('-created_at')[:10]
    recent_requests = ServiceRequest.objects.order_by('-created_at')[:10]
    recent_providers = User.objects.filter(role='provider').order_by('-date_joined')[:10]
    recent_images = ProviderWorkImage.objects.order_by('-uploaded_at')[:12]

    context = {
        'total_clients': total_clients,
        'total_providers': total_providers,
        'total_searches': total_searches,
        'total_requests': total_requests,
        'completed_jobs': completed_jobs,
        'cancelled_jobs': cancelled_jobs,
        'pending_requests': pending_requests,
        'total_work_images': total_work_images,
        'total_revenue': total_revenue,
        'total_commission': total_commission,
        'top_services': top_services,
        'most_searched_services': most_searched_services,
        'top_providers': top_providers,
        'recent_searches': recent_searches,
        'recent_requests': recent_requests,
        'recent_providers': recent_providers,
        'recent_images': recent_images,
    }

    return render(request, 'admin_dashboard.html', context)

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

@login_required
def redirect_after_login(request):
    if request.user.is_staff or request.user.role == 'admin':
        return redirect('admin_dashboard')
    return redirect('dashboard')