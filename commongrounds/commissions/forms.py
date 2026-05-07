from django import forms
from .models import JobApplication, Commission, Job
from django.forms import inlineformset_factory


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


JobFormSet = inlineformset_factory(
    Commission, Job,
    fields=['role', 'manpower_required', 'status'],
    extra=3,
    can_delete=True,
    max_num=3
)

JobFormSet.form.base_fields['role'].required = False
JobFormSet.form.base_fields['manpower_required'].required = False
