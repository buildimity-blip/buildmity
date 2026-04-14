from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    # Home & Auth
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('signup/client/', views.signup_client, name='signup_client'),
    path('signup/provider/', views.signup_provider, name='signup_provider'),
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('redirect-after-login/', views.redirect_after_login, name='redirect_after_login'),
    
    # Search
    path('client-search/', views.client_search, name='client_search'),
    path('all-services/', views.all_services, name='all_services'),
    path('search-providers/', views.search_providers, name='search_providers'),
    
    # Service Needs
    path('create-service-need/', views.create_service_need, name='create_service_need'),
    path('service-need/<int:need_id>/providers/', views.match_providers, name='match_providers'),
    
    # Service Requests
    path('client-requests/', views.client_requests, name='client_requests'),
    path('provider-requests/', views.provider_requests, name='provider_requests'),
    path('request-service/<int:provider_id>/', views.request_service, name='request_service'),
    path('request-service/<int:provider_id>/<int:need_id>/', views.request_service, name='request_service_with_need'),
    path('request/<int:request_id>/', views.service_request_detail, name='service_request_detail'),
    path('update-request-status/<int:request_id>/<str:status>/', views.update_request_status, name='update_request_status'),
    
    # Negotiations & Payments
    path('request/<int:request_id>/negotiation/', views.negotiation_room, name='negotiation_room'),
    path('request/<int:request_id>/payment/', views.make_payment, name='make_payment'),
    path('request/<int:request_id>/release/', views.release_payment, name='release_payment'),
    
    # Job Completion & Ratings
    path('confirm-completion/<int:request_id>/', views.confirm_completion, name='confirm_completion'),
    path('rate-provider/<int:request_id>/', views.rate_provider, name='rate_provider'),
    path('provider-ratings/<int:provider_id>/', views.provider_ratings, name='provider_ratings'),
    path('provider-confirm-completion/<int:request_id>/', views.provider_confirm_completion, name='provider_confirm_completion'),
    
    # Payment Popup
    path('payment-popup/<str:transaction_id>/', views.payment_popup, name='payment_popup'),
    path('confirm-payment/<str:transaction_id>/', views.confirm_payment, name='confirm_payment'),
    
    # Provider Profile
    path('provider/profile/', views.provider_profile, name='provider_profile'),
    path('provider/<int:provider_id>/', views.provider_detail, name='provider_detail'),
    path('upload-work-image/', views.upload_work_image, name='upload_work_image'),
    
    # Admin
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-dashboard/user/<int:user_id>/', views.admin_user_detail, name='admin_user_detail'),
    path('admin-dashboard/user/<int:user_id>/approve/', views.approve_provider, name='approve_provider'),
    path('admin-dashboard/user/<int:user_id>/ignore/', views.ignore_provider, name='ignore_provider'),
    path('admin-dashboard/user/<int:user_id>/suspend/', views.suspend_user, name='suspend_user'),
    
    # Other
    path('robots.txt/', views.robots_txt, name='robots_txt'),
]