from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import (
    ProfileUpdateSerializer,
    RegisterSerializer,
    LoginSerializer,
    ChangePasswordSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer,
)
from core.models import User
from .models import PasswordResetToken
from django.core.mail import send_mail
from django.conf import settings
import uuid
from django.utils import timezone
from datetime import timedelta
import secrets
from django.core.mail import EmailMultiAlternatives


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    "is_superuser": serializer.validated_data["is_superuser"],
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        data = {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "is_staff": user.is_staff,
            "is_superuser": user.is_superuser,
            "date_joined": user.date_joined.isoformat(),
        }
        return Response(data, status=status.HTTP_200_OK)


class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            request.user.set_password(serializer.validated_data["new_password"])
            request.user.save()
            return Response(
                {"detail": "Password changed successfully"}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"].strip().lower()
        user = User.objects.filter(email=email).first()

        # Always return 200 to avoid user enumeration
        if not user:
            return Response(
                {"detail": "If the email exists, a reset link was sent."},
                status=status.HTTP_200_OK,
            )

        # Create token
        token = secrets.token_urlsafe(32)
        expires_at = timezone.now() + timedelta(hours=1)
        PasswordResetToken.objects.create(user=user, token=token, expires_at=expires_at)

        # Build FRONTEND reset link (React page reads ?token=...)
        reset_link = f"{settings.FRONTEND_RESET_URL}?token={token}"

        subject = "Password Reset Request"
        text_body = f"Click the link to reset your password: {reset_link}"
        html_body = f"""
            <div style="font-family:Arial,Helvetica,sans-serif;line-height:1.6">
              <h2 style="margin:0 0 12px">পাসওয়ার্ড রিসেট</h2>
              <p>আপনার পাসওয়ার্ড রিসেট করতে নিচের বাটনে ক্লিক করুন।</p>
              <p>
                <a href="{reset_link}" 
                   style="display:inline-block;background:#ef4444;color:#fff;padding:10px 16px;border-radius:8px;text-decoration:none">
                   Reset Password
                </a>
              </p>
              <p>লিংকটি ১ ঘণ্টা পর্যন্ত কার্যকর থাকবে।</p>
              <p style="font-size:12px;color:#666">যদি আপনি এই অনুরোধ না করে থাকেন, তাহলে এই ইমেলটি উপেক্ষা করুন।</p>
            </div>
        """

        msg = EmailMultiAlternatives(
            subject, text_body, settings.DEFAULT_FROM_EMAIL, [email]
        )
        msg.attach_alternative(html_body, "text/html")
        msg.send(fail_silently=False)

        return Response(
            {"detail": "If the email exists, a reset link was sent."},
            status=status.HTTP_200_OK,
        )


class ResetPasswordView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            reset_token = serializer.validated_data["reset_token"]
            user = reset_token.user
            user.set_password(serializer.validated_data["new_password"])
            user.save()
            reset_token.delete()
            return Response(
                {"detail": "Password reset successfully"}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        data = {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "phone": user.phone,
            "blood_group": user.blood_group,
            "address": user.address,
            "last_donation_date": user.last_donation_date,
            "is_staff": user.is_staff,
            "is_superuser": user.is_superuser,
            "date_joined": user.date_joined.isoformat(),
            "can_donate": self.can_donate(user),
        }
        return Response(data, status=status.HTTP_200_OK)

    def patch(self, request):
        user = request.user
        serializer = ProfileUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def can_donate(self, user):
        if not user.last_donation_date:
            return True
        three_months_ago = timezone.now().date() - timedelta(days=90)
        return user.last_donation_date <= three_months_ago
