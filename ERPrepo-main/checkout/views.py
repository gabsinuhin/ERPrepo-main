from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from requested_inventory.models import ProductRequest
from myapp.models import UserProfile
from .models import CreditMemoRequest
from .forms import CreditMemoRequestForm
from django.shortcuts import render, get_object_or_404
def view_receipt_admin(request, credit_memo_id):
    credit_memo = get_object_or_404(CreditMemoRequest, id=credit_memo_id)

    # Debugging prints
    print(f"Credit Memo ID: {credit_memo.id}")
    print(f"Requested By: {credit_memo.requested_by}")
    print(f"Product Request: {credit_memo.product_request}")

    total_cost = credit_memo.product_request.product.price * credit_memo.product_request.quantity_requested
    tax = total_cost * Decimal('0.001')
    shipping_fee = Decimal('5.00')
    total_with_tax_and_shipping = total_cost + tax + shipping_fee

    # More debugging prints
    print(f"Total Cost: {total_cost}")
    print(f"Tax: {tax}")
    print(f"Shipping Fee: {shipping_fee}")
    print(f"Total with Tax and Shipping: {total_with_tax_and_shipping}")

    context = {
        'credit_memo': credit_memo,
        'total_cost': total_cost,
        'tax': tax,
        'shipping_fee': shipping_fee,
        'total_with_tax_and_shipping': total_with_tax_and_shipping,
    }

    return render(request, 'inventory/view_receipt_admin.html', context)




def view_receipt_admin(request, request_id):
    """View for displaying the receipt of a credit memo request for admin users."""
    credit_memo = get_object_or_404(CreditMemoRequest, id=request_id)

    return render(request, 'inventory/view_receipt_admin.html', {
        'credit_memo': credit_memo,
    })


@login_required
def request_credit_memo(request, request_id):
    """View for users to request a credit memo."""
    product_request = get_object_or_404(ProductRequest, id=request_id)

    if request.method == 'POST':
        form = CreditMemoRequestForm(request.POST)
        if form.is_valid():
            credit_memo_request = form.save(commit=False)
            credit_memo_request.product_request = product_request
            credit_memo_request.requested_by = request.user
            credit_memo_request.save()
            messages.success(request, 'Your credit memo request has been submitted and is pending approval.')
            return redirect('receipt', product_request_id=request_id)
    else:
        form = CreditMemoRequestForm()

    return render(request, 'inventory/request_credit_memo.html', {
        'form': form,
        'product_request': product_request
    })


@staff_member_required
def manage_credit_memo_requests(request):
    """View for superusers to approve or reject credit memo requests."""
    pending_requests = CreditMemoRequest.objects.filter(status='pending')

    if request.method == 'POST':
        request_id = request.POST.get('request_id')
        action = request.POST.get('action')
        credit_memo = get_object_or_404(CreditMemoRequest, id=request_id)
        product_request = credit_memo.product_request
        user_profile = UserProfile.objects.get(user=credit_memo.requested_by)

        if action == 'approve':
            if credit_memo.new_quantity is not None:
                original_quantity = product_request.quantity_requested
                new_quantity = credit_memo.new_quantity

                if new_quantity < original_quantity:
                    original_total = Decimal(product_request.product.price) * Decimal(original_quantity)
                    new_total = Decimal(product_request.product.price) * Decimal(new_quantity)
                    refund_amount = original_total - new_total
                    user_profile.balance += refund_amount
                    user_profile.save()

                    product_request.quantity_requested = new_quantity
                    product_request.save()

                elif new_quantity > original_quantity:
                    original_total = Decimal(product_request.product.price) * Decimal(original_quantity)
                    new_total = Decimal(product_request.product.price) * Decimal(new_quantity)
                    additional_cost = new_total - original_total

                    if user_profile.balance >= additional_cost:
                        user_profile.balance -= additional_cost
                        user_profile.save()

                        product_request.quantity_requested = new_quantity
                        product_request.save()
                    else:
                        messages.error(request, 'Insufficient balance to cover the additional quantity.')
                        return redirect('manage_credit_memo_requests')

            credit_memo.status = 'approved'
            credit_memo.approved_at = timezone.now()
            credit_memo.approved_by = request.user
            credit_memo.save()

            messages.success(request, 'Credit memo request approved and balance updated if applicable.')
        elif action == 'reject':
            credit_memo.status = 'rejected'
            credit_memo.save()
            messages.success(request, 'Credit memo request rejected.')

        return redirect('manage_credit_memo_requests')

    return render(request, 'inventory/manage_credit_memo_requests.html', {
        'pending_requests': pending_requests
    })



@login_required
def process_payment(request, product_request_id):
    """View for processing payments."""
    product_request = get_object_or_404(ProductRequest, id=product_request_id)
    user_profile = get_object_or_404(UserProfile, user=request.user)

    total_cost = Decimal(product_request.product.price) * Decimal(product_request.quantity_requested)
    tax_rate = Decimal('0.001')  # 0.1%
    shipping_fee = Decimal('2.00')  # $2 shipping fee
    tax = total_cost * tax_rate
    total_with_tax_and_shipping = total_cost + tax + shipping_fee

    if request.method == 'POST':
        shipping_address = request.POST.get('shipping_address')
        card_number = request.POST.get('card_number')
        expiry_date = request.POST.get('expiry_date')
        cvv = request.POST.get('cvv')
        currency = request.POST.get('currency')

        # Check if user has enough balance
        if user_profile.balance >= total_with_tax_and_shipping:
            # Deduct the amount from user profile balance
            user_profile.balance -= total_with_tax_and_shipping
            user_profile.save()

            # Update product request status
            product_request.status = 'paid'
            product_request.save()

            # Store receipt data in session
            request.session['receipt_data'] = {
                'total_cost': str(total_cost),
                'tax': str(tax),
                'shipping_fee': str(shipping_fee),
                'total_with_tax_and_shipping': str(total_with_tax_and_shipping),
            }

            # Redirect to the receipt page after successful payment
            return redirect('receipt', product_request_id=product_request.id)  # Use product_request.id

        else:
            # Insufficient balance
            messages.error(request, 'Insufficient balance. Please top up your account .', extra_tags='checkout')
            return redirect('checkout', request_id=product_request.id)  # Ensure this matches your URL pattern

    # If not POST method, redirect to the checkout page
    return redirect('checkout', request_id=product_request.id)  # Ensure this matches your URL pattern




@login_required
def checkout(request, request_id):
    """View for displaying the checkout details."""
    product_request = get_object_or_404(ProductRequest, id=request_id, status='approved')
    user_profile = get_object_or_404(UserProfile, user=request.user)

    total_cost = Decimal(product_request.product.price) * Decimal(product_request.quantity_requested)
    tax_rate = Decimal('0.001')  # 0.1%
    shipping_fee = Decimal('2.00')
    tax = total_cost * tax_rate
    total_with_tax_and_shipping = total_cost + tax + shipping_fee

    balance = user_profile.balance
    adjusted_total = max(total_with_tax_and_shipping - balance, Decimal('0.00'))

    context = {
        'product_request': product_request,
        'total_cost': total_cost,
        'tax': tax,
        'shipping_fee': shipping_fee,
        'total_with_tax_and_shipping': total_with_tax_and_shipping,
        'balance': balance,
        'adjusted_total': adjusted_total,
        'status': product_request.status,
    }
    return render(request, 'inventory/checkout.html', context)


@login_required
def receipt_view(request, product_request_id):
    """View for displaying the receipt, including checkout details."""
    product_request = get_object_or_404(ProductRequest, id=product_request_id)

    # Assuming the user has already checked out this product_request
    total_cost = Decimal(product_request.product.price) * Decimal(product_request.quantity_requested)
    tax_rate = Decimal('0.001')  # 0.1%
    shipping_fee = Decimal('2.00')
    tax = total_cost * tax_rate
    total_with_tax_and_shipping = total_cost + tax + shipping_fee

    user_profile = get_object_or_404(UserProfile, user=request.user)
    balance = user_profile.balance
    adjusted_total = max(total_with_tax_and_shipping - balance, Decimal('0.00'))

    credit_memo = CreditMemoRequest.objects.filter(product_request=product_request).first()

    context = {
        'product_request': product_request,
        'total_cost': total_cost,
        'tax': tax,
        'shipping_fee': shipping_fee,
        'total_with_tax_and_shipping': total_with_tax_and_shipping,
        'balance': balance,
        'adjusted_total': adjusted_total,
        'status': product_request.status,
        'credit_memo': credit_memo,
    }

    return render(request, 'inventory/receipt.html', context)



