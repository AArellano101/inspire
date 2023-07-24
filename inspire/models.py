from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from .managers import *

class InspireUser(AbstractUser):
    favourites = ArrayField(models.PositiveIntegerField(), blank=True, default=list)
    pwcode = models.PositiveIntegerField(blank=True, null=True)
    pwcodecreated = models.DateTimeField(blank=True, null=True)
    emailverified = models.BooleanField(default=False)
    lastunchange = models.DateTimeField(null=True)
    lastpwchange = models.DateTimeField(null=True)
    lastemailchange = models.DateTimeField(null=True)
    notifications = ArrayField(models.PositiveIntegerField(), blank=True, default=list)
    checkednotifications = models.BooleanField(default=True)
    objects = CustomUserManager()

class Favourite(models.Model):
    category = models.CharField(max_length=300)
    postid =  models.CharField(max_length=10)
    objects = FavouriteManager()

class Notification(models.Model):
    noti = models.CharField(max_length=300)
    sent = models.DateTimeField()
    objects = NotificationManager()

class UserMessage(models.Model):
    name = models.CharField(max_length=70, null=True)
    email = models.CharField(max_length=70, null=True)
    message = models.TextField(max_length=1000)
    objects = MessageManager()

class Post(models.Model):
    postid = models.CharField(max_length=10)
    title = models.CharField(max_length=70, null=True)
    created = models.DateTimeField()
    tags = ArrayField(models.CharField(max_length=30), blank=True, default=list)
    category = models.CharField(max_length=50)
    subcategories = ArrayField(models.CharField(max_length=30), default=list)
    description = models.TextField(max_length=1000, null=True)
    featured = models.BooleanField(default=False)
    readablecreated = models.CharField(max_length=50)
    image = models.CharField(max_length=500, null=True)
    likes = models.PositiveIntegerField(default=0)
    objects = PostManager()

    class Meta:
        abstract = True

class Text(Post):
    text = models.TextField(max_length=1000)

class Video(Post):
    src = models.CharField(max_length=200)
    platform = models.CharField(max_length=30)