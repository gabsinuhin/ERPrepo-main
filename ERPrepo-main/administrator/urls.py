from django.urls import path
from . import views

urlpatterns = [
    path('admin_page/', views.admin_page, name='admin_page'),
    # Ensure this line exists

]
