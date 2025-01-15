from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Pet

class PetAdmin(admin.ModelAdmin):
    # Displayed columns in the list view
    list_display = ["name", "display_owner_name", "breed", "age", "display_profile_picture"]
    
    # List filters and search functionality
    list_filter = ["owner", "breed"]
    search_fields = ["name", "breed", "owner__email"]
    ordering = ["name"]
    
    # Fields to be used in the form view (add/edit)
    fields = ["owner", "name", "breed", "age", "profile_picture"]

    # Custom method to display the owner's full name as a clickable link
    def display_owner_name(self, obj):
        if obj.owner:
            # Construct the URL for the user's admin profile (adjust URL name as necessary)
            url = reverse("admin:accounts_customuser_change", args=[obj.owner.id])
            return format_html('<a href="{}" style="color: #007bff; font-weight: bold;">{}</a>', url, f"{obj.owner.first_name} {obj.owner.last_name}")
        return "No Owner"
    display_owner_name.short_description = "Owner Name"

    # Custom method to display the profile picture as a round image in the list view
    def display_profile_picture(self, obj):
        if obj.profile_picture:
            return format_html('<img src="{}" style="border-radius: 50%; width: 50px; height: 50px; object-fit: cover;" />', obj.profile_picture.url)
        return "No image"
    display_profile_picture.short_description = "Profile Picture"

# Register the Pet model with the PetAdmin class
admin.site.register(Pet, PetAdmin)
