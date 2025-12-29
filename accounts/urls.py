from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.signup, name="signup"),            # if you have already
    path("success/", views.success, name="success"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("discover/", views.discover, name="discover"),
    path("profile/<str:username>/", views.profile_view, name="profile"),
    path("like/", views.like_user, name="like_user"),
    path("matches/", views.matches_view, name="matches"),
]