from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from datetime import datetime
from random import randint
import pytz

def readable_datetime(date):
    months = {1:"Jan",2:"Feb",3:"Mar",4:"Apr",5:"May",6:"June",
              7:"July",8:"Aug",9:"Sep",10:"Oct",11:"Nov",12:"Dec"}
    
    month = months[int(date.strftime("%m"))]
    day = date.strftime("%d")
    year = date.strftime("%Y")  
    time = date.strftime("%H:%M")

    return f"{month} {day}, {year} - {time}"

def get_pid(l):
    code = ""
    rules = [
        lambda s: not (a <= 64 and a >=58),
        lambda s: not (a <= 96 and a >=91),
    ]
    it = 0

    while it < l:
        a = randint(48, 122)
        if all(rule(a) for rule in rules):
            code += chr(a)
            it += 1

    return code

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password, favourites=[], **extra_fields):
        user = self.create(username=username, favourites=favourites, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(username, password, **extra_fields)
    
    def add_notification(self, user, id):
        user.notifications.insert(0, id)
        user.save()

    def add_favourite(self, user, fid):
        user.favourites.insert(0, fid)
        user.save()

    def remove_favourite(self, user, fid):
        user.favourites.remove(fid)
        user.save()

class FavouriteManager(models.Manager):
    def create_favourite(self, category, postid):
        f = self.create(category=category, postid=postid)
        f.save()
        return f
    
class MessageManager(models.Manager):
    def create_message(self, name, email, message):
        message = self.create(name=name, email=email, message=message)
        return message
    
class PostManager(models.Manager):
    def create_text(self, title, tags, category, description, text, image):
        text = self.create(title=title, tags=tags, 
            created=datetime.now(pytz.utc), category=category, 
            description=description, text=text, image=image,
            readablecreated=readable_datetime(datetime.now(pytz.utc)))
        
        while True:
            pid = get_pid(10)
            if not self.filter(postid=pid).exists():
                break
        text.postid = pid
        text.save()
        return text
    
    def create_video(self, title, tags, category, description, src, platform):
        video = self.create(title=title, tags=tags, 
            created=datetime.now(pytz.utc), category=category, 
            description=description, readablecreated=readable_datetime(datetime.now(pytz.utc)),
            src=src, platform=platform)
        
        while True:
            pid = get_pid(10)
            if not self.filter(postid=pid).exists():
                break
        video.postid = pid
        video.save()
        return video
    
class NotificationManager(models.Manager):
    def create_notification(self, noti):
        n = self.create(noti=noti, sent=datetime.now(pytz.utc))
        n.save()
        return n
