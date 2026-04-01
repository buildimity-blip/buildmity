from django import forms
from .models import Job


class JobCreateForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['description']
        widgets = {
            'description': forms.Textarea(attrs={
                'rows': 5,
                'placeholder': 'Describe the job you need...'
            })
        }