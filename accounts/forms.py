from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomSignupForm(UserCreationForm):
    age = forms.IntegerField(required=False)
    gender = forms.ChoiceField(choices=CustomUser.gender_choices, required=False)
    bio = forms.CharField(widget=forms.Textarea, required=False)
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = [
            'username', 
            'email', 
            'password1', 
            'password2', 
            'age', 
            'gender', 
            'bio', 
            'profile_picture'
        ]