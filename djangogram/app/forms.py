from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm
from django import forms


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ("email", "username", "password1", "password2")


class EditProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, required=False)
    last_name = forms.CharField(max_length=50, required=False)
    bio = forms.CharField(max_length=150, required=False)
    avatar = forms.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = ("first_name", "last_name", "bio", "email", "avatar")
