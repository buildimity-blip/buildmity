from django.urls import path
from django.contrib.auth import views as auth_views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

urlpatterns = [
    path('', views.dashboard, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),

    path('signup/client/', views.signup_client, name='signup_client'),
    path('signup/provider/', views.signup_provider, name='signup_provider'),

    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('redirect-after-login/', views.redirect_after_login, name='redirect_after_login'),

    path('search-providers/', views.search_providers, name='search_providers'),
    path('provider/<int:provider_id>/', views.provider_detail, name='provider_detail'),
    path('provider/profile/', views.provider_profile, name='provider_profile'),

    path('service-need/create/', views.create_service_need, name='create_service_need'),
    path('service-need/<int:need_id>/providers/', views.match_providers, name='match_providers'),

    path('request-service/<int:provider_id>/', views.request_service, name='request_service'),
    path('request-service/<int:provider_id>/<int:need_id>/', views.request_service, name='request_service_with_need'),

    path('client-requests/', views.client_requests, name='client_requests'),
    path('provider-requests/', views.provider_requests, name='provider_requests'),
    path('provider-requests/<int:request_id>/<str:status>/', views.update_request_status, name='update_request_status'),

    path('request/<int:request_id>/', views.service_request_detail, name='service_request_detail'),
    path('request/<int:request_id>/negotiation/', views.negotiation_room, name='negotiation_room'),
    path('request/<int:request_id>/payment/', views.make_payment, name='make_payment'),
    path('request/<int:request_id>/release/', views.release_payment, name='release_payment'),

    path('upload-work-image/', views.upload_work_image, name='upload_work_image'),

    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-dashboard/user/<int:user_id>/', views.admin_user_detail, name='admin_user_detail'),
    path('admin-dashboard/user/<int:user_id>/approve/', views.approve_provider, name='approve_provider'),
    path('admin-dashboard/user/<int:user_id>/ignore/', views.ignore_provider, name='ignore_provider'),
    path('admin-dashboard/user/<int:user_id>/suspend/', views.suspend_user, name='suspend_user'),
]