import json
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import InventoryAccessRequest
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import logging
from django.shortcuts import get_object_or_404, redirect
from .models import InventoryAccessRequest  # Replace with your actual mode
logger = logging.getLogger(__name__)



def approve_inventory_request(request, id):  # Make sure 'id' is included here
    request_obj = get_object_or_404(InventoryAccessRequest, id=id)
    # Logic to approve the request
    request_obj.status = 'inventory_approved'  # Or whatever logic you need
    request_obj.save()
    return redirect('admin_page')  # Redirect to your desired page


@login_required
def decline_inventory_request(request, id):  # Change 'request_id' to 'id'
    """Decline an inventory access request."""
    request_obj = get_object_or_404(InventoryAccessRequest, id=id)  # Use 'id' here
    request_obj.status = 'inventory_declined'  # Set the status to declined
    request_obj.save()
    messages.success(request, "Inventory request declined successfully!")  # Optional message
    return redirect('admin_page')  # Redirect to the admin page



@login_required
def delete_inventory_request(request, request_id):
    """Delete an inventory access request."""
    user_request = get_object_or_404(InventoryAccessRequest, id=request_id)
    if request.user.is_superuser:
        user_request.delete()
        logger.info(f"Request with ID {request_id} deleted by superuser {request.user.username}.")
        messages.success(request, "Inventory request deleted successfully!")
    else:
        messages.error(request, "You do not have permission to delete this request.")
    return redirect('admin_page')

@login_required
def submit_inventory_request(request):
    """Submit a new inventory access request."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            item = data.get('item')

            # Check if the user already has a pending or approved request
            if InventoryAccessRequest.objects.filter(user=request.user, status__in=['inventory_approved', 'inventory_pending']).exists():
                return JsonResponse({'status': 'error', 'message': 'You already have a pending or approved request.'})

            # Create a new request
            new_request = InventoryAccessRequest(user=request.user, item=item)
            new_request.save()

            return JsonResponse({
                'status': 'success',
                'item': item,
                'date': new_request.created_at.strftime("%Y-%m-%d %H:%M:%S")
            })
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data.'})
        except Exception as e:
            logger.error(f"Error in submit_inventory_request: {str(e)}")
            return JsonResponse({'status': 'error', 'message': 'An error occurred.'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

@login_required
def requested_inventory(request):
    """Display the requested inventory."""
    return render(request, 'inventory/requested_inventory.html')

@login_required
def homepage_view(request):
    """Display the homepage with user requests."""
    user_requests = InventoryAccessRequest.objects.filter(user=request.user)
    logger.info(f"User requests: {user_requests}")

    approved_requests_count = user_requests.filter(status='inventory_approved').count()

    return render(request, 'users/homepage.html', {
        'requests': user_requests,
        'approved_requests_count': approved_requests_count,
    })
