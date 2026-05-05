# users/adapters.py
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.utils import user_email
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    """
    Custom adapter to handle existing email conflicts during Google login
    and auto-generate usernames for new users
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
    
    def populate_user(self, request, sociallogin, data):
        """
        Populate user with data from social provider
        Auto-generate username from email if not provided
        """
        user = super().populate_user(request, sociallogin, data)
        
        # Auto-generate username from email if username is empty
        if not user.username or user.username == '':
            email = user.email or data.get('email', '')
            if email:
                # Take part before @ as username
                username = email.split('@')[0]
                # Remove special characters
                username = ''.join(c for c in username if c.isalnum() or c == '_')
                # Make sure it's unique
                base_username = username
                counter = 1
                while User.objects.filter(username=username).exists():
                    username = f"{base_username}{counter}"
                    counter += 1
                user.username = username
        
        return user
    
    def save_user(self, request, sociallogin, form=None):
        """
        Save user and ensure they have a role
        """
        user = super().save_user(request, sociallogin, form)
        
        # Set default role if not set
        if not user.role:
            user.role = 'client'
            user.save()
        
        return user
