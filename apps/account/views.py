from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    LogoutSerializer,
    RefreshTokenSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer,
    VerifyEmailSerializer,
)
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from apps.emails.utils import send_password_reset_email

User = get_user_model()


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"message": "User registered successfully"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data["login"]
            password = serializer.validated_data["password"]
            user = authenticate(request=request, username=username, password=password)
            if user:
                refresh = RefreshToken.for_user(user)
                return Response(
                    {
                        "refresh_token": str(refresh),
                        "access_token": str(refresh.access_token),
                    }
                )
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        if serializer.is_valid():
            try:
                # Extract the token from the serializer
                refresh_token = serializer.validated_data["refresh_token"]
                # Attempt to blacklist the given token
                token = RefreshToken(refresh_token)
                token.blacklist()
                # Return a successful logout message
                return Response(
                    {"message": "User logged out successfully"},
                    status=status.HTTP_204_NO_CONTENT,
                )
            except TokenError as e:
                # If the token can't be blacklisted or any other error arises, handle it
                return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        # If the serializer is not valid, return an error
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RefreshTokenView(APIView):
    def post(self, request):
        serializer = RefreshTokenSerializer(data=request.data)
        if serializer.is_valid():
            try:
                # Create a new token instance from the provided refresh token
                refresh = RefreshToken(serializer.validated_data["refresh_token"])
                # Generate a new access and refresh token
                data = {
                    "access_token": str(refresh.access_token),
                    "refresh_token": str(
                        refresh
                    ),  # Optionally return the new refresh token
                }
                return Response(data, status=status.HTTP_200_OK)
            except TokenError as e:
                # Handle error that might occur during token refresh process
                return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordView(APIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            # Retrieve user based on the validated email
            user = User.objects.get(email=email)

            # Generate token and encode UID
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            # Construct the reset URL
            reset_url = f"https://api.yourcard.au/reset-password/{uid}/{token}/"  # Adjust the domain as needed

            # Send the password reset email
            send_password_reset_email(user.email, reset_url)

            return Response(
                {"message": "Password reset email sent."}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            token = serializer.validated_data.get("token")
            password = serializer.validated_data.get("password")

            # Verify the token
            user = User.objects.filter(pk=token).first()
            if user is None or not default_token_generator.check_token(user, token):
                return Response(
                    {"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST
                )

            # Update user's password
            user.set_password(password)
            user.save()

            return Response(
                {"message": "Password reset successfully"}, status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendVerificationEmailView(APIView):
    def post(self, request):
        # Email verification logic here
        return Response(
            {"message": "Email verified successfully"}, status=status.HTTP_200_OK
        )


class VerifyEmailView(APIView):
    def post(self, request):
        serializer = VerifyEmailSerializer(data=request.data)
        if serializer.is_valid():
            # Email verification logic here
            return Response(
                {"message": "Email verified successfully"}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
