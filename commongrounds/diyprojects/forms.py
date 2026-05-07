from django import forms
from .models import Project, ProjectReview, ProjectRating


class ProjectForm(forms.ModelForm):
    creator = forms.CharField()

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['creator'].initial = self.user.profile
        self.fields['creator'].disabled = True

    class Meta:
        model = Project
        fields = ['title', 'category', 'creator','description', 'materials', 'steps', 'status']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = ProjectReview
        fields = ['comment', 'image']


class RatingForm(forms.ModelForm):
    class Meta:
        model = ProjectRating
        fields = ['score']
