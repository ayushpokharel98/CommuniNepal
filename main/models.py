from django.db import models
import uuid
from datetime import datetime
from django.contrib.auth.models import User
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_images', default='blank-profile-picture.png')
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pp = models.ImageField()
    post_picture = models.ImageField(upload_to='posts')
    content = models.CharField(max_length=400)
    created_at = models.DateTimeField(default=datetime.now)
    no_of_likes = models.IntegerField(default=0)
    
    def __str__(self):
        return self.user.username
