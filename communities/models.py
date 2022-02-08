from django.db import models
from accounts.models import User
from accounts.validators import validate_image

class Community(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=130)
    created_at = models.DateTimeField(auto_now_add= True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    participants = models.ManyToManyField(User, blank=True)
    image = models.ImageField(upload_to='community/', validators=[validate_image])

    def __str__(self):
        return f"{self.title}"

    def natural_key(self):
        return self.title