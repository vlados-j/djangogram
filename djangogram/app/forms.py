from .models import CustomUser, Image, Post
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


class PostCreationForm(forms.ModelForm):
    images = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)

    class Meta:
        model = Post
        fields = ['description']

    # def save(self, commit=True):
    #     post = super().save(commit=False)
    #     if commit:
    #         post.save()
    #
    #     for image in self.cleaned_data.get('images', []):
    #         Image.objects.create(post=post, image=image)
    #
    #     return post
