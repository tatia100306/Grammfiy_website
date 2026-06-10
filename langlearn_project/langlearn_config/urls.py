from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Ganti 'admin.site.sender' menjadi 'admin.site.urls'
    path('admin/', admin.site.urls), 
    
    # Menghubungkan ke urls.py milik aplikasi core
    path('', include('core.urls')), 
]