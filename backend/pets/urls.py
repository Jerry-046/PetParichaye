from django.urls import path
from .views import PetCreateView, PetProfileView, PetProfileUpdateView, PetDeleteView

urlpatterns = [
    path('create/', PetCreateView.as_view(), name='create-pet'),
    path('<int:pk>/profile/', PetProfileView.as_view(), name='view-pet-profile'),
    path('<int:pk>/update/', PetProfileUpdateView.as_view(), name='update-pet'),
    path('<int:pk>/delete/', PetDeleteView.as_view(), name='delete-pet'),
]
