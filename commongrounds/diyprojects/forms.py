from django import forms
from .models import Project, ProjectReview, ProjectRating


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ['creator']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = ProjectReview
        fields = ['comment', 'image']


class RatingForm(forms.ModelForm):
    class Meta:
        model = ProjectRating
        fields = ['score']
