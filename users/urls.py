
from django.urls import path
from .views import RegisterView, ProfileView
from rest_framework_simplejwt.views import TokenObtainPairView
from users.views import admin_dashboard,redirect_after_login
urlpatterns = [
 path('register/', RegisterView.as_view()),
 path('login/', TokenObtainPairView.as_view()),
 path('profile/', ProfileView.as_view()),
 path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
 path('redirect-after-login/', redirect_after_login, name='redirect_after_login'),
]
