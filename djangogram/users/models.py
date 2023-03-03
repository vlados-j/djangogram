from django.db import models


class User(models.Model):
    email = models.EmailField(max_length=100, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    bio = models.CharField(max_length=150)
    avatar = models.ImageField() #additional args might be added later
    registered_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
