from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

from django.core.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from .models import UserProfile
# Create your views here.


class SignupUserView(APIView):
    permission_classes = [AllowAny]
    
    
    def post(self, request):
        data = request.data
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        confirm_password = data.get("confirm_password")
        role = data.get("role")
        illness = data.get("illness", "")
        
        
        required_fields = [username, email, password, confirm_password, role]
        if not all(required_fields):
            return Response(
                {"error": "All required fields must be provided."},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        if User.objects.filter(username=username).exists():
            return Response(
                {"error": "Username already exists."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if password != confirm_password:
            return Response(
                {"error": "Passwords do not match."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if role not in ["patient", "supporter"]:
            return Response(
                {"error": "Invalid role."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if role == "patient" and not illness.strip():
            return Response(
                {"error": "Illness is required for patients."},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            validate_password(password)
        except ValidationError as err:
            return Response(
                {"error": err.messages},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        user = User.objects.create_user(username=username, email=email, password=password)
        
        if role == "patient":
            illness_value = illness
        else:
            illness_value = ""
        UserProfile.objects.create(
            user=user,
            role=role,
            illness=illness_value
        )

        
        refresh = RefreshToken.for_user(user)

        return Response({
            "message": "Account created successfully.",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": role,
                "illness": illness_value
            },
            "tokens": {
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            }
        }, status=status.HTTP_201_CREATED)