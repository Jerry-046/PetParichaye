from django.urls import path
from . import views

urlpatterns = [
    path('<int:pet_id>/profile/', views.pet_profile, name='pet_profile'),
]
