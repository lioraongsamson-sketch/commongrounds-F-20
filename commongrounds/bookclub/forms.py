from django import forms
from .models import Book, BookReview, Borrow


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        exclude = ('contributor',)

class BookUpdateForm(forms.ModelForm):
    class Meta:
        model = Book
        exclude = ('contributor',)


class BookReviewForm(forms.ModelForm):
    class Meta:
        model = BookReview
        exclude = ('user_reviewer','anon_reviewer','book',)


class BookBorrowForm(forms.ModelForm):
    class Meta:
        model = Borrow
        fields = ['name', 'date_borrowed',]
        widgets ={
            'date_borrowed': forms.TextInput(
                attrs={'type': 'datetime-local'}
            )
        }