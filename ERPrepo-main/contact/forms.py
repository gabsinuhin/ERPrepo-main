from .models import Message, Reply
from django import forms

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['content', 'image']  # Include the image field for the reply

class ContactForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content', 'image']  # Include the image field for the message
