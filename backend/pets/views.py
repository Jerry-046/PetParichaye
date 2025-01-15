from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Pet
from .serializers import PetSerializer

class PetListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        pets = Pet.objects.filter(owner=request.user)
        serializer = PetSerializer(pets, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data.copy()
        data["owner"] = request.user.id
        serializer = PetSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class PetDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        pet = Pet.objects.filter(pk=pk, owner=request.user).first()
        if not pet:
            return Response({"error": "Pet not found"}, status=404)
        serializer = PetSerializer(pet)
        return Response(serializer.data)

    def put(self, request, pk):
        pet = Pet.objects.filter(pk=pk, owner=request.user).first()
        if not pet:
            return Response({"error": "Pet not found"}, status=404)
        serializer = PetSerializer(pet, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        pet = Pet.objects.filter(pk=pk, owner=request.user).first()
        if not pet:
            return Response({"error": "Pet not found"}, status=404)
        pet.delete()
        return Response({"message": "Pet deleted successfully"}, status=200)
