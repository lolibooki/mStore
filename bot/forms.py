from django import forms
from .models import Customer


class CustomerEditForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('address', 'phone', 'mobile')