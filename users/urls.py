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
    # Dispute URLs
    path('raise-dispute/<int:request_id>/', views.raise_dispute, name='raise_dispute'),
    path('dispute/<int:dispute_id>/', views.dispute_detail, name='dispute_detail'),
    path('admin/disputes/', views.admin_disputes, name='admin_disputes'),
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

    # API URLs
    path('api/', views.api_home, name='api_home'),
    path('api/register/', views.api_register, name='api_register'),
    path('api/profile/', views.api_profile, name='api_profile'),
    path('api/services/', views.api_services, name='api_services'),
    path('api/providers/', views.api_providers, name='api_providers'),
    path('api/my-requests/', views.api_my_requests, name='api_my_requests'),
    path('api/make-payment/<int:request_id>/', views.api_make_payment, name='api_make_payment'),

    # Analytics
    path('analytics/', views.analytics_dashboard, name='analytics_dashboard'),
    path('export-report/<str:report_type>/', views.export_report, name='export_report'),
# Service Checklist
    path('service-checklist/<int:request_id>/', views.service_checklist, name='service_checklist'),
    # Mobile App API URLs
path('api/login/', views.api_login, name='api_login'),
path('api/logout/', views.api_logout, name='api_logout'),
path('api/register/', views.api_register, name='api_register'),
path('api/profile/', views.api_profile, name='api_profile'),
path('api/update-profile/', views.api_update_profile, name='api_update_profile'),
path('api/services/', views.api_services, name='api_services'),
path('api/providers/', views.api_providers, name='api_providers'),
path('api/search-providers/', views.api_search_providers, name='api_search_providers'),
path('api/provider/<int:provider_id>/', views.api_provider_detail, name='api_provider_detail'),
path('api/my-requests/', views.api_my_requests, name='api_my_requests'),
path('api/create-request/', views.api_create_service_request, name='api_create_service_request'),
path('api/dashboard-stats/', views.api_dashboard_stats, name='api_dashboard_stats'),
path('api/notifications/', views.api_notifications, name='api_notifications'),
path('my-referrals/', views.my_referrals, name='my_referrals'),
path('api/mark-notification/<int:notification_id>/', views.api_mark_notification_read, name='api_mark_notification_read'),
path('api/make-payment/<int:request_id>/', views.api_make_payment, name='api_make_payment'),
# Location URLs
path('api/update-location/', views.update_user_location, name='update_user_location'),
path('api/nearby-providers/', views.nearby_providers, name='nearby_providers'),
path('api/calculate-trip/', views.calculate_trip, name='calculate_trip'),
# Location URLs
path('update-location/', views.update_location, name='update_location'),
path('nearby-providers/', views.nearby_providers_map, name='nearby_providers'),
path('provider-location/<int:provider_id>/', views.provider_location, name='provider_location'),
path('calculate-route/', views.calculate_route, name='calculate_route'),
path('save-location/<int:request_id>/', views.save_service_location, name='save_location'),
path('api/verify-flutterwave-payment/<str:transaction_id>/', views.verify_flutterwave_payment, name='verify_flutterwave_payment'),
  # Admin provider management User
 # Provider management URLs (without /admin/ prefix)
path('approve-provider/<int:user_id>/', views.approve_provider, name='approve_provider'),
path('ignore-provider/<int:user_id>/', views.ignore_provider, name='ignore_provider'),
path('suspend-user/<int:user_id>/', views.suspend_user, name='suspend_user'),
path('admin-user/<int:user_id>/', views.admin_user_detail, name='admin_user_detail'),
# Flutterwave URLs
path('payment/initialize/<int:request_id>/', views.initialize_flutterwave_payment, name='initialize_flutterwave_payment'),
path('payment/callback/<str:tx_ref>/', views.payment_callback, name='payment_callback'),
path('payment/webhook/flutterwave/', views.flutterwave_webhook, name='flutterwave_webhook'),
path('payment/initialize/<int:request_id>/', views.initialize_flutterwave_payment, name='initialize_flutterwave_payment'),
path('request/<int:request_id>/payment/', views.make_payment, name='make_payment'),
path('confirm-payment/<str:transaction_id>/', views.confirm_payment, name='confirm_payment'),
# Add these to your urlpatterns

# Chat URLs
path('chat/conversations/', views.conversations, name='conversations'),
path('chat/conversation/<int:conversation_id>/', views.conversation_detail, name='conversation_detail'),
path('chat/start/<int:user_id>/', views.start_conversation, name='start_conversation'),
path('chat/unread-count/', views.get_unread_count, name='unread_count'),

# Booking URLs
path('booking/create/<int:request_id>/', views.create_booking, name='create_booking'),
path('booking/update/<int:booking_id>/<str:status>/', views.update_booking_status, name='update_booking_status'),
path('booking/provider-availability/', views.provider_availability, name='provider_availability'),
path('booking/add-time-off/', views.add_time_off, name='add_time_off'),

# Invoice URLs
path('invoice/generate/<int:request_id>/', views.generate_invoice, name='generate_invoice'),
path('invoice/download/<int:invoice_id>/', views.download_invoice, name='download_invoice'),

# Promo Code URLs
path('promo/apply/<int:request_id>/', views.apply_promo_code, name='apply_promo_code'),

# Withdrawal URLs
path('withdrawal/request/', views.request_withdrawal, name='request_withdrawal'),
path('withdrawal/my-withdrawals/', views.my_withdrawals, name='my_withdrawals'),
path('admin/withdrawals/', views.admin_withdrawals, name='admin_withdrawals'),

# Favorites URLs
path('favorites/toggle/<int:provider_id>/', views.toggle_favorite, name='toggle_favorite'),
path('favorites/my/', views.my_favorites, name='my_favorites'),

# Locations URLs
path('locations/saved/', views.saved_locations, name='saved_locations'),
path('locations/delete/<int:location_id>/', views.delete_saved_location, name='delete_saved_location'),

# Notifications URLs
path('notifications/', views.notification_center, name='notification_center'),
path('notifications/preferences/', views.notification_preferences, name='notification_preferences'),
    # Live Location Tracking URLs
path('api/location/update/', views.update_live_location, name='update_live_location'),
path('api/location/get/<int:user_id>/', views.get_user_location, name='get_user_location'),
path('admin/location/tracker/', views.admin_location_tracker, name='admin_location_tracker'),
path('admin/location/history/<int:user_id>/', views.user_location_history, name='user_location_history'),
path('api/providers/nearby-live/', views.nearby_providers_live, name='nearby_providers_live'),
path('api/service/<int:request_id>/track/', views.track_service_location, name='track_service_location'),
]
]
