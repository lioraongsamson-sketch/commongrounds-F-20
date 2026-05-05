from django import forms
from .models import Book, BookReview


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = "__all__"

class BookUpdateForm(forms.ModelForm):
    class Meta:
        model = Book
        exclude = ('contributor',)


class BookReviewForm(forms.ModelForm):
    class Meta:
        model = BookReview
        fields = ["title", "comment"]
