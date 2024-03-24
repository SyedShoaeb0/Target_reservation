"""
URL configuration for My_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from authentication import views as auth_views  # Import your authentication views

urlpatterns = [
    path('admin/', admin.site.urls),  # Django admin route
    path('login/', auth_views.login_view, name='login_view'),  # Your custom login view
    path('logout/', auth_views.logout_user, name='logout'),  # Your custom logout view
    path('register/', auth_views.register, name='register'),  # Your custom registration view
    path('book_target/', auth_views.book_target, name='book_target'),  # Custom view to book a target
    path('release_target/', auth_views.release_target, name='release_target'),
]