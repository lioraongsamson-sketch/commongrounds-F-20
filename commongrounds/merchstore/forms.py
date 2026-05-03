from django import forms
from .models import Transaction, Product

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'product_type', 'product_image','description',
                  'price','stock','status']
        