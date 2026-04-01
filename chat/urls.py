from django.urls import path
from . import views

urlpatterns = [
    path('send/', views.send_message),
    path('messages/<int:user1_id>/<int:user2_id>/', views.get_messages),
]