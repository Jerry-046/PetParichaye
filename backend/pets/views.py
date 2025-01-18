from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Pet, MedicalReport
from .serializers import PetSerializer, MedicalReportSerializer
from rest_framework import status
from django.shortcuts import render, get_object_or_404
from .models import Pet

def pet_profile(request, pet_id):
    # Get the pet object or return 404 if it doesn't exist
    pet = get_object_or_404(Pet, id=pet_id)
    return render(request, 'pet_profile.html', {'pet': pet})

class PetViewSet(viewsets.ModelViewSet):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer

    @action(detail=True, methods=['get'])
    def qr_code(self, request, pk=None):
        pet = self.get_object()
        return Response({
            "qr_code_url": pet.qr_code.url
        })

