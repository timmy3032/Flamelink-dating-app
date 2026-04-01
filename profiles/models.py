from django.db import models
from django.conf import settings


# ---------------------
# Profile
# ---------------------
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to="profile_pics/", blank=True, null=True)

    def __str__(self):
        return self.user.username


# ---------------------
# Like
# ---------------------
class Like(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='likes_sent', on_delete=models.CASCADE)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='likes_received', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('sender', 'receiver')  # 🔥 Prevent duplicate likes

    def __str__(self):
        return f"{self.sender} ❤️ {self.receiver}"


# ---------------------
# Match
# ---------------------
class Match(models.Model):
    user1 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='matches_user1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='matches_user2', on_delete=models.CASCADE)
    matched_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user1', 'user2')  # 🔥 Prevent duplicate matches

    def __str__(self):
        return f"{self.user1} 🤝 {self.user2}"