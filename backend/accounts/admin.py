from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser

    # List fields to be displayed in the admin
    list_display = ["email", "first_name", "last_name", "is_active", "is_staff", "profile_picture_preview_list"]

    # Custom method to display the profile picture preview in the list view
    def profile_picture_preview_list(self, obj):
        if obj.profile_picture:
            return format_html('<img src="{}" style="border-radius: 50%; width: 50px; height: 50px; object-fit: cover;" />', obj.profile_picture.url)
        return "No Image"
    profile_picture_preview_list.short_description = "Profile Picture (List)"

    # Custom method to display the profile picture preview in the general tab (form view)
    def profile_picture_preview(self, obj):
        if obj.profile_picture:
            return format_html('<img src="{}" style="border-radius: 50%; width: 200px; height: 200px; object-fit: cover; display: block; margin-left: auto; margin-right: auto;" />', obj.profile_picture.url)
        return "No Image"
    profile_picture_preview.short_description = "Profile Picture"

    # Modify fieldsets to include the profile picture preview in the general tab without label
    fieldsets = (
        (None, {
            "fields": ("profile_picture_preview", "first_name", "last_name", "email" )  # Only once here
        }),
        ("Personal Info", {
            "fields": ("bio", "address", "profile_picture", "is_active", "is_staff")  # Removed duplicated fields
        }),
        ("Permissions", {
            "fields": ("is_superuser", "groups", "user_permissions")  # Removed duplicated fields
        }),
        ("Important Dates", {
            "fields": ("last_login",)
        }),
    )

    # Add fieldsets for creating a new user (if required)
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("first_name", "last_name","email", "password1", "password2","address","bio", "profile_picture"),
        }),
    )

    # Make the profile picture preview readonly in the form
    readonly_fields = ("profile_picture_preview",)

    # Set ordering for the CustomUser model in the admin
    ordering = ["email"]


# Register CustomUser model with the Django admin site
admin.site.register(CustomUser, CustomUserAdmin)
