# urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),
    path('inventory/', include('inventory.urls')),
    path('administrator/', include('administrator.urls')),
    path('contact/', include('contact.urls')),
    path('requested_inventory/', include('requested_inventory.urls')),
    path('checkout/', include('checkout.urls')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
