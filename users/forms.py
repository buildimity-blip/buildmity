from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class ClientSignUpForm(UserCreationForm):
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


from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, ProviderWorkImage


class ClientSignUpForm(UserCreationForm):
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


class ProviderSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    service_name = forms.CharField(required=True)
    phone_number = forms.CharField(required=True)
    location = forms.CharField(required=True)
    bio = forms.CharField(widget=forms.Textarea, required=False)
    profile_photo = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'service_name',
            'phone_number',
            'location',
            'bio',
            'profile_photo',
            'password1',
            'password2',
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.role = User.PROVIDER
        user.service_name = self.cleaned_data['service_name']
        user.phone_number = self.cleaned_data['phone_number']
        user.location = self.cleaned_data['location']
        user.bio = self.cleaned_data['bio']
        user.profile_photo = self.cleaned_data.get('profile_photo')
        if commit:
            user.save()
        return user


class ProviderWorkImageForm(forms.ModelForm):
    class Meta:
        model = ProviderWorkImage
        fields = ['image', 'caption']