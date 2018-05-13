from django import forms
from .models import Product, Purchase


class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'price', 'count', 'image')


class PurchaseEditForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ('product_count',)


class ProductEditForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('price', 'count', 'image')