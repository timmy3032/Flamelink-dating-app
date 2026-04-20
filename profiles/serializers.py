from rest_framework import serializers
from accounts.models import CustomUser
from .models import Profile, Like, Match


# PROFILE
class ProfileSerializer(serializers.ModelSerializer):
    photo = serializers.ImageField(use_url=True)

    class Meta:
        model = Profile
        fields = ['bio', 'photo']


# USER (IMPORTANT)
class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'age', 'gender', 'profile']


# LIKE
class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'


# MATCH
class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = '__all__'