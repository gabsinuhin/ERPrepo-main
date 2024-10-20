from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Automatically assigned
    content = models.TextField()
    image = models.ImageField(upload_to='messages/', blank=True, null=True)  # New image field
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

class Reply(models.Model):
    message = models.ForeignKey(Message, related_name='replies', on_delete=models.CASCADE)  # Link to a specific message
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # User who replied
    content = models.TextField()
    image = models.ImageField(upload_to='replies/', blank=True, null=True)  # New image field
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reply by {self.user.username} on {self.created_at}"
