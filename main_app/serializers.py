from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, Post, PostComment, PostLike, Donation


class UserSerilaizer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True, required=True)
    confirm_password = serializers.CharField(write_only = True, required=True)
    
    class Meta: 
        model = User
        fields = ['id', 'username', 'email', 'password', 'confirm_password']
        
    
    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Password do not match")
        return data
    
    
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        return user
