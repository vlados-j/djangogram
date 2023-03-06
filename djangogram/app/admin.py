from django.contrib import admin
from .models import User, Post, Like, Tag, Image

admin.site.register(User)
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Tag)
admin.site.register(Image)
