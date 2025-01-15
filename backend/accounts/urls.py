from django.urls import path
from .views import RegisterView, LoginView, LogoutView, ChangeProfilePictureView, ResetPasswordView,ConfirmPasswordView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    path('reset-password/confirm/', ConfirmPasswordView.as_view(), name='confirm-password'),
]
