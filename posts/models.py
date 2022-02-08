from django.db import models
from accounts.models import User
from communities.models import Community

class Post(models.Model):
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to='image/')
    created_at = models.DateTimeField(auto_now_add= True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    community = models.ForeignKey(Community, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.title} | {self.user.username}"

class Comment(models.Model):
    text = models.TextField(max_length=180)
    created_at = models.DateTimeField(auto_now_add= True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.text} | {self.post.id}"

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add= True, blank=True)

    def __str__(self):
        return f"{self.user}, {self.post}"