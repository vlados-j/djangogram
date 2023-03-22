from django.contrib import admin
from .models import CustomUser, Post, Like, Tag, Image
from django.contrib.auth.admin import UserAdmin
from .forms import RegisterForm


class CustomUserAdmin(UserAdmin):
    add_form = RegisterForm
    model = CustomUser
    list_display = ["email", "username", ]


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Tag)
admin.site.register(Image)
