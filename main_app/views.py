from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny, IsAuthenticated

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

from django.core.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from .models import UserProfile, Post
from .serializers import UserProfileSerializer, UserSerializer, PostSerializer
# Create your views here.

class PostListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        profile = get_object_or_404(UserProfile, user=user)
        if profile.role == 'patient':
            posts = Post.objects.filter(patient=user)
        else:
            posts = Post.objects.all()

        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, request):
        user = request.user
        profile = get_object_or_404(UserProfile, user=user)

        if profile.role != 'patient':
            return Response({'error': 'Only patients can create posts.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(patient=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)

        if post.patient != request.user:
            return Response({'error': 'You can edit only your own posts.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def delete(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        print("Patient:", post.patient.id, "User:", request.user.id)

        if post.patient != request.user:
            return Response({'error': 'You can delete only your own posts.'}, status=status.HTTP_403_FORBIDDEN)

        post.delete()
        return Response({'message': 'Post deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)




class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get_profile_data(self, user, serializer):
        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": serializer.data.get("role"),
            "illness": serializer.data.get("illness"),
            "created_at": serializer.data.get("created_at"),
        }

    def get(self, request):
        profile = get_object_or_404(UserProfile, user=request.user)
        serializer = UserProfileSerializer(profile)
        data = self.get_profile_data(request.user, serializer)
        return Response(data, status=status.HTTP_200_OK)

    def put(self, request):
        profile = get_object_or_404(UserProfile, user=request.user)
        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            data = self.get_profile_data(request.user, serializer)
            return Response({
                "message": "Profile updated successfully.",
                "profile": data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
class SignupUserView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        print("Incoming signup data:", request.data)
        
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
                "firstName":user.first_name,
                "lastName":user.last_name,
                "username": user.username,
                "email": user.email,
                "role": role,
                "illness": illness_value
            },
            "tokens": {
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            }, 
        }, status=status.HTTP_201_CREATED)
        


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {"error": "Username and password are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(username=username, password=password)
        if not user:
            return Response(
                {"error": "Invalid username or password."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        refresh = RefreshToken.for_user(user)
        user_data = UserSerializer(user).data

        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": user_data
            },
            status=status.HTTP_200_OK
        )

