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
    """Provider registration with MULTIPLE service selection"""
    
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(required=True)
    location = forms.CharField(required=True)
    bio = forms.CharField(widget=forms.Textarea, required=False)
    profile_photo = forms.ImageField(required=False)
    
    # Multiple service selection - CHANGE TO required=False for now
    services = forms.ModelMultipleChoiceField(
        queryset=Service.objects.filter(is_active=True),
        required=False,  # Change to False since new_service can be used
        widget=forms.CheckboxSelectMultiple()  # Change to checkboxes for better UX
    )
    
    # For adding new service
    new_service = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., Smart Home Installation, Solar Panel Repair'
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
            if field not in ['services', 'new_service']:
                self.fields[field].widget.attrs.update({
                    'class': 'form-control', 
                    'style': 'width:100%; padding:12px; border-radius:8px;'
                })
    
    def clean(self):
        cleaned_data = super().clean()
        services = cleaned_data.get('services')
        new_service = cleaned_data.get('new_service')
        
        # Allow either services OR new_service
        if not services and not new_service:
            raise forms.ValidationError("Please select at least one service or add a new one")
        
        # If new service is provided, check if it exists or create it
        if new_service:
            existing_service = Service.objects.filter(name__iexact=new_service).first()
            if existing_service:
                cleaned_data['new_service_obj'] = existing_service
            else:
                # Create new service on the fly
                cleaned_data['new_service_obj'] = Service.objects.create(
                    name=new_service.title().strip(),
                    description=f"Added by provider",
                    is_active=True
                )
        
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
            
            # Clear existing services
            user.services.clear()
            
            # Add selected services from dropdown
            selected_services = self.cleaned_data.get('services')
            if selected_services:
                user.services.add(*selected_services)
            
            # Add new service if provided
            new_service_obj = self.cleaned_data.get('new_service_obj')
            if new_service_obj:
                user.services.add(new_service_obj)
            
            # For backward compatibility - set first service as main
            if user.services.exists():
                user.service = user.services.first()
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