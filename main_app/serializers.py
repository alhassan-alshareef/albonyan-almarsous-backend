from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, Post, PostComment, PostLike, Donation


class UserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source="userprofile.role", read_only=True)
    illness = serializers.CharField(source="userprofile.illness", read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "role", "illness"]



class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = ["id", "user", "role", "illness", "created_at"]



class PostSerializer(serializers.ModelSerializer):
    patient = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = "__all__"


class PostCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostComment
        fields = "__all__"


class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = "__all__"


class DonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        fields = "__all__"
        read_only_fields = ["patient", "amount_donated", "is_active", "created_at"]