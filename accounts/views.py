from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse, HttpResponseForbidden
from .models import CustomUser, Like, Match
from django.db import IntegrityError

# LOGIN
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('discover')
        else:
            return render(request, "login.html", {"error": "Invalid credentials"})
    return render(request, "login.html")


# LOGOUT
def logout_view(request):
    logout(request)
    return redirect('login')


# SIGNUP
from .forms import CustomSignupForm

def signup(request):
    if request.method == "POST":
        form = CustomSignupForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("success")
        return render(request, "signup.html", {"form": form})
    
    form = CustomSignupForm()
    return render(request, "signup.html", {"form": form})


def success(request):
    return render(request, "success.html")


# DISCOVER USERS
@login_required
def discover(request):
    users = CustomUser.objects.exclude(id=request.user.id)
    return render(request, "discover.html", {"users": users})


# PROFILE VIEW
@login_required
def profile_view(request, username):
    user = get_object_or_404(CustomUser, username=username)
    return render(request, "profile.html", {"profile_user": user})


# LIKE USER API
@login_required
def like_user(request):
    if request.method != "POST":
        return HttpResponseForbidden()

    receiver_id = request.POST.get("receiver_id")
    receiver = get_object_or_404(CustomUser, id=receiver_id)
    sender = request.user

    if sender == receiver:
        return JsonResponse({"status": "error", "message": "Cannot like yourself"})

    try:
        Like.objects.create(sender=sender, receiver=receiver)
    except IntegrityError:
        return JsonResponse({"status": "error", "message": "Already liked"})

    # Check for mutual likes
    mutual = Like.objects.filter(sender=receiver, receiver=sender).exists()
    if mutual:
        u1, u2 = (sender, receiver) if sender.id < receiver.id else (receiver, sender)
        Match.objects.get_or_create(user1=u1, user2=u2)
        return JsonResponse({"status": "match", "message": "It's a match!"})

    return JsonResponse({"status": "ok", "message": "Liked"})


# MATCHES
@login_required
def matches_view(request):
    matches1 = Match.objects.filter(user1=request.user)
    matches2 = Match.objects.filter(user2=request.user)
    matches = [m.user2 for m in matches1] + [m.user1 for m in matches2]
    return render(request, "matches.html", {"matches": matches})