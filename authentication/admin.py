from django.contrib import admin
from .models import CustomUser, Rack, Target

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['email', 'is_active', 'is_staff']
    search_fields = ['email']  # Allow searching by email
    list_filter = ['is_active', 'is_staff']
    # other custom settings

@admin.register(Rack)
class RackAdmin(admin.ModelAdmin):
    pass
    # custom settings for Rack

@admin.register(Target)
class TargetAdmin(admin.ModelAdmin):
    pass
    # custom settings for Target

