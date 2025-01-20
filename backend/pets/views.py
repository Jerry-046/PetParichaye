from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateDestroyAPIView, CreateAPIView, DestroyAPIView
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from .models import Pet
from .serializers import (
    PetCreateSerializer,
    PetProfileViewSerializer,
    PetProfileUpdateSerializer,
)
from .permissions import IsOwnerPermission

class PetCreateView(CreateAPIView):
    serializer_class = PetCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class PetProfileView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
        pet = get_object_or_404(Pet, pk=pk)
        serializer = PetProfileViewSerializer(pet)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PetProfileUpdateView(RetrieveUpdateDestroyAPIView):
    queryset = Pet.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwnerPermission]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return PetProfileUpdateSerializer
        return PetProfileViewSerializer

    def get_object(self):
        pet = get_object_or_404(Pet, pk=self.kwargs['pk'])
        if pet.owner != self.request.user:
            raise PermissionDenied("You do not have permission to modify this pet.")
        return pet

class PetDeleteView(DestroyAPIView):
    queryset = Pet.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwnerPermission]

    def get_object(self):
        pet = get_object_or_404(Pet, pk=self.kwargs['pk'])
        if pet.owner != self.request.user:
            raise PermissionDenied("You do not have permission to delete this pet.")
        return pet

    def destroy(self, request, *args, **kwargs):
        pet = self.get_object()
        owner = pet.owner  # Save owner details before deletion
        pet_name = pet.name  # Save pet name
        self.perform_destroy(pet)
        return Response({
            "message": f"Pet '{pet_name}' has been successfully deleted.",
            "owner": {
                "username": owner.first_name,
                "email": owner.email
            }
        }, status=status.HTTP_200_OK)
