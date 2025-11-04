from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, Post, PostComment, PostLike, Donation,DonationPayment


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
    patient = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = "__all__"

    def get_patient(self, obj):
        return {
            "id": obj.patient.id,
            "username": obj.patient.username,
            "first_name": obj.patient.first_name,
            "last_name": obj.patient.last_name,
        }

    def get_comments_count(self, obj):
        return PostComment.objects.filter(post=obj).count()

    def get_likes_count(self, obj):
        return PostLike.objects.filter(post=obj).count()


class PostCommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = PostComment
        fields = ["id", "post", "user", "username", "content", "created_at"]
        read_only_fields = ["id", "user", "created_at"]


class PostLikeSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = PostLike
        fields = ["id", "post", "user", "username", "created_at"]
        read_only_fields = ["id", "user", "created_at"]




class DonationPaymentSerializer(serializers.ModelSerializer):
    supporter = serializers.HiddenField(default=serializers.CurrentUserDefault())
    supporter_info = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = DonationPayment
        fields = ["id", "donation", "supporter", "supporter_info","amount", "created_at"]
        read_only_fields = ["id", "supporter_info", "created_at"]
        
    def get_supporter_info(self, obj):
        return {
            "id": obj.supporter.id,
            "username": obj.supporter.username
        }


class DonationSerializer(serializers.ModelSerializer):
    patient = UserSerializer(read_only=True)
    payments = DonationPaymentSerializer(many=True, read_only=True)
    progress_percentage = serializers.SerializerMethodField()

    class Meta:
        model = Donation
        fields = "__all__"
        read_only_fields = ["patient", "amount_donated", "is_active", "created_at"]

    def get_progress_percentage(self, obj):
        if not obj.target_amount:
            return 0
        return round((obj.amount_donated / obj.target_amount) * 100, 2)