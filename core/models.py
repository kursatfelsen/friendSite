from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class FriendGroup(models.Model):
    name = models.CharField(max_length=50)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

    def get_friends(self):
        return list(self.friend_set.all())

class Friend(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    friendGroup = models.ManyToManyField(FriendGroup)

    def __str__(self):
        return self.user.username

class Event(models.Model):
    name = models.TextField(max_length=50)
    date = models.DateTimeField()
    location = models.TextField()
    group = models.ForeignKey(FriendGroup, on_delete=models.CASCADE)

    def __str__(self):
        return self.name