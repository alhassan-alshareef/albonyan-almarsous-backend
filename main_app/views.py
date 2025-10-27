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
from .serializers import UserProfileSerializer
# Create your views here.


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        profile = get_object_or_404(UserProfile, user=user)

        serializer = UserProfileSerializer(profile)
        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": serializer.data.get("role"),
            "illness": serializer.data.get("illness"),
            "created_at": serializer.data.get("created_at")
        }, status=status.HTTP_200_OK)



        
class SignupUserView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        data = request.data
        first_name = data.get("first_name", "")
        last_name = data.get("last_name", "")
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        confirm_password = data.get("confirm_password")
        role = data.get("role")
        illness = data.get("illness", "")
        
        
        required_fields = [username, email, password, confirm_password, role, first_name, last_name]
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
            
        user = User.objects.create_user(username=username,email=email,password=password,first_name=first_name,last_name=last_name)
        
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
                "first_name": user.first_name,
                "last_name": user.last_name,
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