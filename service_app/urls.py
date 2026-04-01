from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.conf import settings
from django.conf.urls.static import static

from users.views import (
    signup_client,
    signup_provider,
    search_providers,
    provider_detail,
    request_service,
    client_requests,
    provider_requests,
    upload_work_image,
)


def home(request):
    return JsonResponse({"status": "running"})


@login_required
def dashboard(request):
    context = {
        'role': request.user.role,
    }
    return render(request, 'dashboard.html', context)


urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),

    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('signup/client/', signup_client, name='signup_client'),
    path('signup/provider/', signup_provider, name='signup_provider'),

    path('dashboard/', dashboard, name='dashboard'),

    path('providers/search/', search_providers, name='search_providers'),
    path('providers/<int:provider_id>/', provider_detail, name='provider_detail'),
    path('providers/<int:provider_id>/request/', request_service, name='request_service'),

    path('requests/client/', client_requests, name='client_requests'),
    path('requests/provider/', provider_requests, name='provider_requests'),

    path('provider/work/upload/', upload_work_image, name='upload_work_image'),

    path('jobs/', include('jobs.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)