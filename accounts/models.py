from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
from . validators import validate_image

class User(AbstractUser):
    email = models.EmailField(unique=True)
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)
    image = models.ImageField(upload_to='profile/', validators=[validate_image])

    def get_date(self):
        time = datetime.now()
        if self.date_joined.day == time.day:
            return str(time.hour - self.date_joined.hour) + " hours ago"
        else:
            if self.date_joined.month == time.month:
                return str(time.day - self.date_joined.day) + " days ago"
            else:
                if self.date_joined.year == time.year:
                    return str(time.month - self.date_joined.month) + " months ago"
        
        return self.created_at