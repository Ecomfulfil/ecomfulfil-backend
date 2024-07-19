from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['email', 'username', 'first_name', 'last_name', 'is_staff', 'image']  # Customize as needed
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('image',)}),  # Add the image field to the admin
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('image',)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)