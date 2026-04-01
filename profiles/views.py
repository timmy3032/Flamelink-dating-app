from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser

from accounts.models import CustomUser
from .models import Profile, Like, Match
from .serializers import UserSerializer, MatchSerializer, ProfileSerializer

from django.contrib.auth import authenticate


# ---------------------
# Register
# ---------------------
@api_view(['POST'])
def register(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    age = request.data.get('age')
    gender = request.data.get('gender')

    if CustomUser.objects.filter(username=username).exists():
        return Response({"error": "Username already exists"}, status=400)

    user = CustomUser.objects.create_user(
        username=username,
        email=email,
        password=password,
        age=age,
        gender=gender
    )

    Profile.objects.create(user=user)

    return Response({"message": "User registered successfully"}, status=201)


# ---------------------
# Login
# ---------------------
@api_view(['POST'])
def login(request):
    user = authenticate(
        username=request.data.get('username'),
        password=request.data.get('password')
    )

    if user:
        return Response({
            "message": "Login successful",
            "user": UserSerializer(user).data
        })

    return Response({"error": "Invalid credentials"}, status=401)


# ---------------------
# Dashboard
# ---------------------
@api_view(['GET'])
def dashboard(request):
    users = CustomUser.objects.all()
    return Response(UserSerializer(users, many=True).data)


# ---------------------
# Like
# ---------------------
@api_view(['POST'])
def like_user(request):
    sender_id = request.data.get('sender_id')
    receiver_id = request.data.get('receiver_id')

    try:
        sender = CustomUser.objects.get(id=sender_id)
        receiver = CustomUser.objects.get(id=receiver_id)
    except:
        return Response({"error": "User not found"}, status=404)

    Like.objects.get_or_create(sender=sender, receiver=receiver)

    # MATCH LOGIC
    if Like.objects.filter(sender=receiver, receiver=sender).exists():

        exists = Match.objects.filter(user1=sender, user2=receiver).exists() or \
                 Match.objects.filter(user1=receiver, user2=sender).exists()

        if not exists:
            Match.objects.create(user1=sender, user2=receiver)

        return Response({"message": "It's a MATCH! ❤️"})

    return Response({"message": "User liked!"})


# ---------------------
# Matches
# ---------------------
@api_view(['GET'])
def matches(request, user_id):
    matches = Match.objects.filter(user1_id=user_id) | Match.objects.filter(user2_id=user_id)
    return Response(MatchSerializer(matches.distinct(), many=True).data)


# ---------------------
# GET PROFILE ✅ (THIS FIXES YOUR ERROR)
# ---------------------
@api_view(['GET'])
def get_profile(request, user_id):
    try:
        user = CustomUser.objects.get(id=user_id)
        profile = Profile.objects.get(user=user)
        return Response(ProfileSerializer(profile).data)
    except:
        return Response({"error": "Profile not found"}, status=404)


# ---------------------
# UPLOAD PHOTO
# ---------------------
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def upload_profile_photo(request):
    user_id = request.data.get('user_id')
    photo = request.FILES.get('photo')

    if not user_id or not photo:
        return Response({"error": "user_id and photo required"}, status=400)

    try:
        user = CustomUser.objects.get(id=user_id)
        profile = Profile.objects.get(user=user)
    except:
        return Response({"error": "User/Profile not found"}, status=404)

    profile.photo = photo
    profile.save()

    return Response({
        "message": "Uploaded successfully",
        "photo_url": profile.photo.url
    })