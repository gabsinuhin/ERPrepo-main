from django.urls import path
from . import views

urlpatterns = [
    # Checkout process
    path('checkout/<int:request_id>/', views.checkout, name='checkout'),
    path('process_payment/<int:product_request_id>/', views.process_payment, name='process_payment'),
    path('checkout/receipt/<int:product_request_id>/', views.receipt_view, name='receipt'),

    # Credit Memo Request process
    path('request-credit-memo/<int:request_id>/', views.request_credit_memo, name='request_credit_memo'),
    path('manage-credit-memos/', views.manage_credit_memo_requests, name='manage_credit_memo_requests'),
    path('checkout/view_receipt/<int:request_id>/', views.view_receipt_admin, name='view_receipt_admin'),

]
