from django.db import models
from django.contrib.auth.models import User

class InventoryAccessRequest(models.Model):
    STATUS_CHOICES = [
        ('inventory_pending', 'Waiting for Inventory Approval'),
        ('inventory_approved', 'Inventory Approved'),
        ('inventory_declined', 'Inventory Declined'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the user who made the request
    item = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='inventory_pending')  # Update the field to match the new status choices

    def __str__(self):
        return f"{self.created_at} - {self.item} by {self.user.username} ({self.status})"  # Show status in the string representation
