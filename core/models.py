from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class FriendGroup(models.Model):
    name = models.CharField(max_length=50)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    img_url = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def get_friends(self):
        return list(self.friend_set.all())

class Friend(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    friendGroup = models.ManyToManyField(FriendGroup,blank=True)

    first_name = models.CharField(max_length=50,blank=True)
    second_name = models.CharField(max_length=50,blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.user.username


class Event(models.Model):
    PROPOSED = 'P1'
    PLANNED = 'P2'
    HAPPENING = 'H1'
    HAPPENED = 'H2'
    STATE_CHOICES = [
        (PROPOSED, 'Proposed'),
        (PLANNED, 'Planned'),
        (HAPPENING, 'Happening'),
        (HAPPENED, 'Happened'),
    ]
    name = models.TextField(max_length=50)
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    location = models.TextField(null=True)
    group = models.ForeignKey(FriendGroup, on_delete=models.CASCADE)
    state = models.CharField(
        max_length=2,
        choices=STATE_CHOICES,
        default=PROPOSED,
    )
    ranking = models.IntegerField(null=True,default=0)
    def __str__(self):
        return self.name

    def getYeas(self):
        return Vote.objects.filter(event__id = self.id, status=True).count()
    def getNas(self):
        return Vote.objects.filter(event__id = self.id, status=False).count()

class Vote(models.Model):
    event = models.ForeignKey(Event,on_delete=models.CASCADE)
    friend = models.ForeignKey(Friend,on_delete=models.CASCADE)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.friend}'s vote on {self.event}: {self.status}"