from django.urls import path
from . import views  # Ensure this imports the views defined above



urlpatterns = [
    path('approve_request/<int:id>/', views.approve_inventory_request, name='approve_inventory_request'),
    path('decline_request/<int:id>/', views.decline_inventory_request, name='decline_inventory_request'),
    path('delete-inventory-request/<int:request_id>/', views.delete_inventory_request, name='delete_inventory_request'),
    path('submit-request/', views.submit_inventory_request, name='submit_inventory_request'),
    path('homepage/', views.homepage_view, name='homepage'),
    path('requested_inventory/', views.requested_inventory, name='requested_inventory'),
    # Add other URL patterns as necessary
]
