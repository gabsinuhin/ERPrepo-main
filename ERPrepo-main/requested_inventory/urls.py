from django.urls import path
from .views import (
    requested_inventory,
    add_product_request,
    add_product,
    view_requested_products,
    all_product_requests,
    approve_request,
    decline_request,
    delete_product_request,
    delete_product,
    delete_product_view,
    update_stock,
    update_product,
    cancel_request,
    search_products


)

urlpatterns = [
    # ... other URL patterns ...
    path('requested_inventory/', requested_inventory, name='requested_inventory'),
    path('add-product-request/', add_product_request, name='add_product_request'),
    path('add-product/', add_product, name='add_product'),
    path('requested-products/', view_requested_products, name='view_requested_products'),
    path('all-products-request/', all_product_requests, name='all_products_request'),
    path('approve-request/<int:request_id>/', approve_request, name='approve_request'),
    path('decline-request/<int:request_id>/', decline_request, name='decline_request'),
    path('product-requests/delete/<int:request_id>/', delete_product_request, name='delete_product_request'),

    path('update_stock/<int:product_id>/', update_stock, name='update_stock'),  # Add this line
    path('update_product/<int:product_id>/', update_product, name='update_product'),

    path('all-product-request', all_product_requests, name='all_product_requests'),
    path('delete_product/<int:product_id>/', delete_product, name='delete_product'),
    path('cancel_request/<pk>/', cancel_request, name='cancel_request'),
    path('search/', search_products, name='search_products'),

]




