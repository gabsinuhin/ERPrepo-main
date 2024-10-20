from django.db import models
from django.contrib.auth.models import User
from requested_inventory.models import ProductRequest

class CreditMemoRequest(models.Model):
    product_request = models.ForeignKey(ProductRequest, on_delete=models.CASCADE)
    requested_by = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.TextField()
    new_quantity = models.PositiveIntegerField(null=True, blank=True)  # Field for the new quantity
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approver')

    def __str__(self):
        return f"Credit Memo Request for {self.product_request}"


