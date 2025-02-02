from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import RegisterSerializer, LoginSerializer,ResetPasswordSerializer,ConfirmPasswordSerializer,ChangeProfilePictureSerializer,UpdateProfileSerializer,UserProfileSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.utils.translation import gettext_lazy as _
from rest_framework import status, permissions


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=201)
        return Response(serializer.errors, status=400)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data)
        return Response(serializer.errors, status=400)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logged out successfully"}, status=200)
        return Response({"error": "Refresh token required"}, status=400)

class ChangeProfilePictureView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def put(self, request):
        user = request.user
        user.profile_picture = request.data.get("profile_picture")
        user.save()
        return Response({"message": "Profile picture updated successfully"}, status=200)

class ResetPasswordView(APIView):
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            response_data = serializer.save()
            return Response(response_data, status=200)
        return Response(serializer.errors, status=400)
    
class ConfirmPasswordView(APIView):
    def post(self, request):
        serializer = ConfirmPasswordSerializer(data=request.data)
        if serializer.is_valid():
            response_data = serializer.save()
            return Response(response_data, status=200)
        return Response(serializer.errors, status=400)\
        
class ChangeProfilePictureView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        user = request.user
        serializer = ChangeProfilePictureSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Profile picture updated successfully.",
                "profile_picture": user.profile_picture.url  # Return the new picture URL for React
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UpdateProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        serializer = UpdateProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile updated successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)