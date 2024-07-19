from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    LogoutView,
    RefreshTokenView,
    ForgotPasswordView,
    ResetPasswordView,
    SendVerificationEmailView,
    VerifyEmailView
)

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('refresh-tokens', RefreshTokenView.as_view(), name='refresh-tokens'),
    path('forgot-password', ForgotPasswordView.as_view(), name='forgot-password'),
    path('reset-password', ResetPasswordView.as_view(), name='reset-password'),
    path('send-verification-email', SendVerificationEmailView.as_view(), name='send-verification-email'),
    path('verify-email', VerifyEmailView.as_view(), name='verify-email'),
]