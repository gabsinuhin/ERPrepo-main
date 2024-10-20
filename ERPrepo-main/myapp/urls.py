from django.urls import path
from . import views
from django.contrib.auth import views as auth_views  # Ensure this line is present

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('register/', views.register, name='register'),  # Registration page
    path('profile/', views.profile, name='profile'),  # Profile page
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),  # Login page
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),  # Logout page

    path('homepage/', views.homepage, name='homepage'),  # Correct reference to homepage view
    path('inventory/', views.inventory, name='inventory'),  # Correct reference to inventory view
    path('edit_profile/', views.edit_profile, name='edit_profile'),  # Edit profile page
    path('show_all_users/', views.show_all_users, name='show_all_users'),  # Show all users page
    path('users/terminate/<int:user_id>/', views.terminate_account, name='terminate_account'),  # Terminate user account
    path('cash_in/', views.cash_in, name='cash_in'),  # Cash in page
]
