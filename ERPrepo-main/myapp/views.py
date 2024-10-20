from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserProfileEditForm, CashInForm, UserRegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from django.contrib.auth.models import User


@login_required
def cash_in(request):
    if request.method == 'POST':
        form = CashInForm(request.POST)
        if form.is_valid():
            # Extracting form data
            amount = form.cleaned_data['amount']
            card_number = form.cleaned_data['card_number']
            card_expiry = form.cleaned_data['card_expiry']
            card_cvv = form.cleaned_data['card_cvv']

            # Validate credit card details
            if not card_number.isdigit() or len(card_number) != 16:
                messages.error(request, 'Invalid credit card number.')
            elif len(card_expiry) != 5 or card_expiry[2] != '/':
                messages.error(request, 'Invalid expiry date format. Use MM/YY.')
            elif not card_cvv.isdigit() or len(card_cvv) != 3:
                messages.error(request, 'Invalid CVV code.')
            else:
                # Update user's balance
                user_profile = UserProfile.objects.get(user=request.user)
                user_profile.balance += amount
                user_profile.save()
                messages.success(request, f'You have successfully added ${amount:.2f} to your balance.')
                return redirect('cash_in')  # Redirect to avoid form resubmission
    else:
        form = CashInForm()

    return render(request, 'users/cash_in.html', {'form': form})


@login_required
def terminate_account(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user_profile = get_object_or_404(UserProfile, user=user)

    if request.method == 'POST':
        user_profile.delete()  # Delete the user's profile
        user.delete()  # Delete the user
        messages.success(request, f'Account for {user.username} has been terminated successfully!')
        return redirect('show_all_users')  # Redirect to the user list page after deletion

    return render(request, 'inventory/show_all_users.html', {'user': user})


@login_required
def edit_profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileEditForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')  # Redirect to the profile page after saving
    else:
        form = UserProfileEditForm(instance=user_profile)

    return render(request, 'users/profile.html', {'form': form})


def home(request):
    return render(request, 'users/home.html')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Save user without committing
            user.set_password(form.cleaned_data['password'])  # Hash the password
            user.save()  # Now save the user with hashed password

            # Create a UserProfile instance for the newly registered user with the form data
            UserProfile.objects.create(
                user=user,
                company_name=form.cleaned_data['company_name'],
                full_name=form.cleaned_data['full_name'],
                mobile_number=form.cleaned_data['mobile_number'],
                business_title=form.cleaned_data['business_title']
            )
            messages.success(request, 'Your account has been created! You can now log in.')
            return redirect('login')  # Redirect to login or another page after registration
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})


def homepage(request):
    return render(request, 'users/homepage.html')


@login_required
def profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileEditForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        form = UserProfileEditForm(instance=user_profile)

    return render(request, 'users/profile.html', {
        'user': request.user,
        'user_profile': user_profile,
        'balance': user_profile.balance,  # Pass the balance to the template
        'form': form
    })


def inventory(request):
    return render(request, 'users/inventory.html')


def show_all_users(request):
    users = User.objects.all()
    user_profiles = UserProfile.objects.all()

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        new_balance = request.POST.get(f'balance_{user_id}')

        if user_id and new_balance:
            try:
                # Get the user profile based on the user ID
                user_profile = get_object_or_404(UserProfile, user_id=user_id)
                user_profile.balance = float(new_balance)
                user_profile.save()
                messages.success(request, f'Balance for {user_profile.full_name} updated successfully!')
            except ValueError:
                messages.error(request, 'Please enter a valid number for the balance.')

        return redirect('show_all_users')

    # Render the template for GET requests or after POST redirects
    return render(request, 'inventory/show_all_users.html', {
        'users': users,
        'user_profiles': user_profiles
    })
