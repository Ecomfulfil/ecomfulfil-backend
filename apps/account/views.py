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
from rest_framework_simplejwt.tokens import (
    RefreshToken,
    AccessToken,
    TokenError,
    SlidingToken,
    UntypedToken,
)
from rest_framework_simplejwt.token_blacklist.models import (
    BlacklistedToken,
)
from django.contrib.auth import get_user_model
from apps.emails.utils import send_password_reset_email
from django.conf import settings
import jwt
from datetime import datetime, timedelta, timezone

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
            user = User.objects.get(email=email)

            # Generate access token
            access_token = str(AccessToken.for_user(user))

            # Construct the reset URL
            reset_url = f"{settings.HOST_URL}/reset-password/{access_token}/"

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

            try:
                access_token = AccessToken(token)
                user_id = access_token["user_id"]

                user = User.objects.get(id=user_id)

                # Blacklist the token
                blacklisted_token, created = BlacklistedToken.objects.get_or_create(
                    token=token
                )
                if not created:
                    return Response(
                        {"error": "Token has already been used"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            except TokenError as e:
                print(f"Token error: {e}")
                return Response(
                    {"error": "Invalid or expired token"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            except User.DoesNotExist as e:
                print(f"User does not exist error: {e}")
                return Response(
                    {"error": "Invalid or expired token"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            except Exception as e:
                print(f"Unexpected error: {e}")
                return Response(
                    {"error": "An unexpected error occurred"},
                    status=status.HTTP_400_BAD_REQUEST,
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
