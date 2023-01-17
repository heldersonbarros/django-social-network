from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
from . validators import validate_image

class User(AbstractUser):
    email = models.EmailField(unique=True)
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)
    image = models.ImageField(upload_to='profile/', validators=[], blank=True, default='profile/600x600.png')