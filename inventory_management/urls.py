from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api/', include('inventory.urls')),
    path('api/', include('accounts.urls')),
    path('admin/', admin.site.urls),
]
