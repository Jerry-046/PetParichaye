from rest_framework import serializers
from .models import Pet, MedicalReport
from accounts.models import CustomUser

class MedicalReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalReport
        fields = ['report_image', 'description']

class PetCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = ['id', 'name', 'breed', 'age', 'profile_picture']

class PetProfileViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = ['id', 'name', 'breed', 'age', 'profile_picture', 'qr_code','owner']

class PetProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = ['name', 'breed', 'age', 'profile_picture']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'address', 'bio', 'profile_picture']