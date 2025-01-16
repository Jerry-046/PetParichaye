from rest_framework import serializers
from .models import Pet, MedicalReport

class MedicalReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalReport
        fields = ['report_image', 'description']

class PetSerializer(serializers.ModelSerializer):
    medical_reports = MedicalReportSerializer(many=True, read_only=True)
    qr_code = serializers.ImageField(read_only=True)

    class Meta:
        model = Pet
        fields = ['id', 'name', 'breed', 'age', 'profile_picture', 'medical_reports', 'qr_code']
