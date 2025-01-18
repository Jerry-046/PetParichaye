from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PetViewSet, pet_profile

# Create a router and register the PetViewSet
router = DefaultRouter()
router.register(r'pets', PetViewSet)

urlpatterns = [
    # API URLs for PetViewSet
    path('api/', include(router.urls)),
    
    # URL for pet profile page
    path('pets/<int:pet_id>/profile/', pet_profile, name='pet_profile'),
]
