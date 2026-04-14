from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Service, SuggestedService, ProviderWorkImage, Rating


class ClientSignUpForm(UserCreationForm):
    """Client registration form"""
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.role = User.CLIENT
        if commit:
            user.save()
        return user


class ProviderSignupForm(UserCreationForm):
    """Provider registration with service selection - NEW SERVICE ADDED TO DATABASE AUTOMATICALLY"""
    
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(required=True)
    location = forms.CharField(required=True)
    bio = forms.CharField(widget=forms.Textarea, required=False)
    profile_photo = forms.ImageField(required=False)
    
    # Service selection fields
    service = forms.ModelChoiceField(
        queryset=Service.objects.filter(is_active=True),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control', 'style': 'width:100%; padding:12px; border-radius:8px;'})
    )
    new_service = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'e.g., Plumbing, Electrical, Cleaning, Carpentry, Painting',
            'style': 'width:100%; padding:12px; border-radius:8px;'
        })
    )
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'password1', 'password2',
            'phone_number', 'location', 'bio', 'profile_photo'
        ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Style all fields
        for field in self.fields:
            if field not in ['service', 'new_service']:
                self.fields[field].widget.attrs.update({'class': 'form-control', 'style': 'width:100%; padding:12px; border-radius:8px;'})
        
        # Update service field queryset to ensure it's fresh
        self.fields['service'].queryset = Service.objects.filter(is_active=True)
    
    def clean(self):
        cleaned_data = super().clean()
        service = cleaned_data.get('service')
        new_service = cleaned_data.get('new_service')
        
        if not service and not new_service:
            raise forms.ValidationError("Please select a service or add a new one")
        
        # Check if new service name already exists
        if new_service:
            existing_service = Service.objects.filter(name__iexact=new_service).first()
            if existing_service:
                # If it exists, automatically select it and clear new_service
                cleaned_data['service'] = existing_service
                cleaned_data['new_service'] = ''
        
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.role = User.PROVIDER
        user.phone_number = self.cleaned_data['phone_number']
        user.location = self.cleaned_data['location']
        user.bio = self.cleaned_data['bio']
        
        if self.cleaned_data.get('profile_photo'):
            user.profile_photo = self.cleaned_data['profile_photo']
        
        if commit:
            user.save()
            
            # Handle service assignment
            service = self.cleaned_data.get('service')
            new_service_name = self.cleaned_data.get('new_service')
            
            if service:
                # Use existing service
                user.service = service
                user.save()
                
            elif new_service_name:
                # Check if service already exists (double-check)
                existing_service = Service.objects.filter(name__iexact=new_service_name).first()
                if existing_service:
                    user.service = existing_service
                    user.save()
                else:
                    # Create new service - INSTANTLY ADDED TO DATABASE
                    new_service = Service.objects.create(
                        name=new_service_name.title().strip(),
                        description=f"Added by provider {user.username}",
                        is_active=True
                    )
                    user.service = new_service
                    user.save()
        
        return user


class ProviderWorkImageForm(forms.ModelForm):
    """Form for providers to upload work images"""
    class Meta:
        model = ProviderWorkImage
        fields = ['image', 'caption']
        widgets = {
            'caption': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Optional description'}),
        }


class ClientSearchForm(forms.Form):
    """Client search for services and providers"""
    search_query = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search for a service... e.g., Plumbing, Electrical, Cleaning',
            'style': 'width:100%; padding:12px; border-radius:8px;'
        })
    )


class RatingForm(forms.ModelForm):
    """Form for clients to rate providers"""
    
    class Meta:
        model = Rating
        fields = ['rating', 'review']
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-control'}),
            'review': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Share your experience with this provider...'
            }),
        }