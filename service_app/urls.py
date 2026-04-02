from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from users.views import (
    signup_client,
    signup_provider,
    search_providers,
    provider_detail,
    request_service,
    client_requests,
    provider_requests,
    upload_work_image,
    admin_dashboard,   # add this
    redirect_after_login,
)

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html', {'role': request.user.role})

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),

    path('accounts/', include('allauth.urls')),

    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('signup/client/', signup_client, name='signup_client'),
    path('signup/provider/', signup_provider, name='signup_provider'),

    path('dashboard/', dashboard, name='dashboard'),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),  # add this

    path('providers/search/', search_providers, name='search_providers'),
    path('providers/<int:provider_id>/', provider_detail, name='provider_detail'),
    path('providers/<int:provider_id>/request/', request_service, name='request_service'),

    path('requests/client/', client_requests, name='client_requests'),
    path('requests/provider/', provider_requests, name='provider_requests'),

    path('provider/work/upload/', upload_work_image, name='upload_work_image'),

    path('jobs/', include('jobs.urls')),
    path('redirect-after-login/', redirect_after_login, name='redirect_after_login'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)