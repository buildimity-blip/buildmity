# users/adapters.py
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.utils import user_email
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    """
    Custom adapter to handle existing email conflicts during Google login
    """
    
    def pre_social_login(self, request, sociallogin):
        """
        If a user with the same email already exists, connect the social account
        to the existing user instead of creating a new one.
        """
        email = sociallogin.account.extra_data.get('email')
        
        if not email:
            return
        
        try:
            existing_user = User.objects.get(email=email)
            # Connect the social account to the existing user
            sociallogin.connect(request, existing_user)
        except User.DoesNotExist:
            pass
    
    def is_auto_signup_allowed(self, request, sociallogin):
        """
        Allow auto signup for all social accounts
        """
        return True