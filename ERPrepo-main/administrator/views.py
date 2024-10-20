from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test, login_required  # Ensure login_required is imported
from inventory.models import InventoryAccessRequest  # Ensure this is the correct model name
import logging  # Import logging module

# Set up logger
logger = logging.getLogger(__name__)

# Check if the user is an admin
def is_admin(user):
    return user.is_superuser

@login_required  # Ensure the user is logged in
def admin_page(request):
    all_requests = InventoryAccessRequest.objects.all().order_by('-created_at')  # Fetch all requests
    logger.info(f"All requests: {all_requests}")  # Log all requests
    context = {
        'requests': all_requests,
    }
    return render(request, 'users/admin_page.html', context)
