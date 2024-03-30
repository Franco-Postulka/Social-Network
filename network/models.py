from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Profile(models.Model):
    user =  models.ForeignKey(User, on_delete = models.CASCADE, related_name='profile_user')
    follower = models.ForeignKey(User, on_delete= models.CASCADE, related_name='follower')


class Post(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name='post_user')
    text = models.CharField(max_length=280)
    date = models.DateTimeField(default=timezone.now())

    likes = models.ManyToManyField(User,blank=True, related_name='likes')