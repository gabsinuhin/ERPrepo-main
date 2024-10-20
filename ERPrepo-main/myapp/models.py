from django.db import models
from django.contrib.auth.models import User
from django import forms

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=15)
    business_title = models.CharField(max_length=255)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Add this line

    def __str__(self):
        return self.full_name



class UserProfileEditForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['company_name', 'full_name', 'mobile_number', 'business_title', 'balance']  # Include balance



