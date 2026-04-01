from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    age = models.PositiveIntegerField(null=True, blank=True)

    gender_choices = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )

    gender = models.CharField(max_length=1, choices=gender_choices, null=True, blank=True)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    def __str__(self):
        return self.username