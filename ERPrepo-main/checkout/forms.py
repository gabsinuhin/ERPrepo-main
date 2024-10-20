from django import forms
from requested_inventory.models import ProductRequest
from .models import CreditMemoRequest, ProductRequest


class ProductRequestEditForm(forms.ModelForm):
    class Meta:
        model = ProductRequest
        fields = ['quantity_requested', 'status']  # Add other fields you want to allow editing



class CreditMemoRequestForm(forms.ModelForm):
    class Meta:
        model = CreditMemoRequest
        fields = ['reason', 'new_quantity']
        widgets = {
            'reason': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Please provide a reason for the credit memo.'}),
            'new_quantity': forms.NumberInput(attrs={'placeholder': 'Enter new requested quantity'}),
        }
