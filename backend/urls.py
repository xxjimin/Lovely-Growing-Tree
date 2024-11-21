from django.contrib import admin
from django.urls import path, include
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', include('myapp.urls')),  # Assuming the 'myapp' app handles registration
    path('', views.register),  # Redirect root URL to the registration page
]
