from django import forms
from .models import JobApplication, Commission

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['job', 'applicant']
        widgets = {
            'job': forms.HiddenInput(),
            'applicant': forms.HiddenInput(),
        }

class CommissionForm(forms.ModelForm):
    class Meta:
        model = Commission
        fields = ['title', 'description', 'type', 'people_required', 'status']
        widgets = {
            'status': forms.Select(),
        }