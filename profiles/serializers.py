from rest_framework import serializers
from accounts.models import CustomUser
from .models import Profile, Like, Match


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'age', 'gender', 'bio', 'profile_picture']


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'


class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = '__all__'

       
class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')

    class Meta:
        model = Profile
        fields = ['username', 'bio', 'photo']