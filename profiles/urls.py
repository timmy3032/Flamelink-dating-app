from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register),
    path('login/', views.login),
    path('dashboard/', views.dashboard),
    path('like/', views.like_user),
    path('matches/<int:user_id>/', views.matches),
    path('profile/<int:user_id>/', views.get_profile),  # ✅ FIXED
    path('profile/upload/', views.upload_profile_photo),
]