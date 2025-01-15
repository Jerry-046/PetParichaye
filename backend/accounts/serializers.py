from rest_framework import serializers
from .models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

# Serializer to handle User information
class UserSerializer(serializers.ModelSerializer):
    # Including the profile_picture in the response
    class Meta:
        model = CustomUser
        fields = ["id", "email", "first_name", "last_name", "address", "bio", "profile_picture"]

# Serializer to register a new user
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Password field will not be included in responses

    class Meta:
        model = CustomUser
        fields = ["email", "password", "first_name", "last_name", "address", "bio", "profile_picture"]

    def create(self, validated_data):
        # Create a new user with the given data and set the password
        password = validated_data.pop('password')
        user = CustomUser.objects.create_user(**validated_data)
        user.set_password(password)  # Ensure password is hashed before saving
        user.save()
        return user

# Serializer for login (returning JWT tokens)
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()  # Email for user login
    password = serializers.CharField(write_only=True)  # Password field to login the user

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        # Check if the user exists and password is correct
        user = CustomUser.objects.filter(email=email).first()
        if user and user.check_password(password):
            # If valid credentials, create JWT tokens
            refresh = RefreshToken.for_user(user)
            return {
                "refresh": str(refresh),  # Refresh token for refreshing access token
                "access": str(refresh.access_token),  # Access token for authentication
                "user": UserSerializer(user).data,  # Return user details
            }
        raise serializers.ValidationError("Invalid credentials")  # Error for invalid credentials

# Serializer to change the profile picture
class ChangeProfilePictureSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(required=True)

    class Meta:
        model = CustomUser
        fields = ['profile_picture']

    def update(self, instance, validated_data):
        instance.profile_picture = validated_data.get('profile_picture', instance.profile_picture)
        instance.save()
        return instance

User = get_user_model()

class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        """
        Check if the user with the given email exists.
        """
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email does not exist.")
        return value

    def save(self):
        """
        Generate a token and send the password reset link via email.
        """
        email = self.validated_data['email']
        user = User.objects.get(email=email)

        # Generate token and UID
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(str(user.pk).encode())

        # Prepare the reset link (adjust this URL to match your frontend)
        reset_link = f"http://127.0.0.1:8000/reset-password/{uid}/{token}/"

        # Context for the email template
        context = {
            'reset_link': reset_link,
            'user': user,
            'logo_url': 'https://your-domain.com/path-to-logo.png',  # Replace with your logo URL
        }

        # Render HTML email content
        html_content = render_to_string('emails/reset_password.html', context)

        # Prepare and send email
        email_message = EmailMessage(
            subject="Password Reset - PetParichaye",
            body=html_content,
            from_email="petparichaye@gmail.com",
            to=[email],
        )
        email_message.content_subtype = "html"  # This is important to send HTML emails
        email_message.send()

        return {"message": "Password reset email sent successfully."}
    

class ConfirmPasswordSerializer(serializers.Serializer):
    uidb64 = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)

    def validate(self, data):
        """
        Validate the token and decode the user ID.
        """
        try:
            # Decode the UID and get the user
            uid = urlsafe_base64_decode(data['uidb64']).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError("Invalid or expired link.")

        # Validate the token
        if not default_token_generator.check_token(user, data['token']):
            raise serializers.ValidationError("Invalid or expired token.")

        # Validate the new password
        validate_password(data['new_password'], user)

        # Attach the user to the validated data
        data['user'] = user
        return data

    def save(self):
        """
        Update the user's password.
        """
        user = self.validated_data['user']
        new_password = self.validated_data['new_password']

        # Set and save the new password
        user.set_password(new_password)
        user.save()
        return {"message": "Password has been reset successfully."}