# RUN THE SCRIPT FROM THE SCRIPTS FOLDER. OTHERWISE, THE SCRIPT WON'T WORK.

import os
import django
from faker import Faker
import sys
from django.core.files.images import ImageFile
from PIL import Image as PILImage

sys.path.append('../')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangogram.settings')
django.setup()

from django.contrib.auth import get_user_model
from app.models import Post, Image

User = get_user_model()

fake = Faker()

# Create 10 users
for i in range(10):
    username = fake.user_name()
    email = fake.email()
    first_name = fake.first_name()
    last_name = fake.last_name()
    bio = fake.text(max_nb_chars=150)
    password = fake.password()
    User.objects.create_user(
        username=username,
        email=email,
        first_name=first_name,
        last_name=last_name,
        bio=bio,
        password=password,
    )

# Create 20 posts
users = User.objects.all()
for i in range(20):
    user = fake.random_element(users)
    description = fake.text(max_nb_chars=1200)
    post = Post.objects.create(
        user=user,
        description=description,
    )

    for each_image in range(2):
        image = PILImage.new('RGB', (800, 600), (247, 202, 201))
        image_path = f'post_{i}_{each_image}.jpg'
        image.save(image_path)

        img = Image.objects.create(
            post=post,
            image=ImageFile(open(image_path, 'rb'))
        )

        os.remove(image_path)