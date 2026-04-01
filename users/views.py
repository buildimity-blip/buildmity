from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from .forms import ClientSignUpForm, ProviderSignUpForm, ProviderWorkImageForm
from .models import User
from jobs.models import ServiceRequest


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
    client_lat = request.GET.get('lat')
    client_lng = request.GET.get('lng')

    providers = User.objects.filter(role='provider')

    if query:
        providers = providers.filter(service_name__icontains=query)

    return render(request, 'search_providers.html', {
        'query': query,
        'providers': providers,
        'client_lat': client_lat,
        'client_lng': client_lng,
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