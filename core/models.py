from django.db import models
from django.contrib.auth.models import User

from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.


class FriendGroup(models.Model):
    name = models.CharField(max_length=50)
    # TODO Wrong foreign key must be friend not user
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    img_url = models.TextField(blank=True)
    is_private = models.BooleanField(blank=True, default=False)
    # friend_set for friendGroup field in Friend
    # event_set for group field in Event

    def __str__(self):
        return self.name

    def get_friends(self):
        return list(self.friend_set.all())


class Friend(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='friend')
    friendGroup = models.ManyToManyField(FriendGroup, blank=True)
    friendWith = models.ManyToManyField('self',blank=True)
    description = models.TextField(blank=True)
    img = models.TextField(blank=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    fullname = models.CharField(max_length=30, blank=True)
    phone = PhoneNumberField(blank=True)
    # event for creator
    # event_set for group field in Event
    # attending_set for attender field in Event
    # vote_set for friend field in Vote

    def __str__(self):
        return self.user.username

    def join_group(self, group_id):
        self.friendGroup.add(FriendGroup.objects.get(id=group_id))

    def leave_group(self, group_id):
        self.friendGroup.remove(FriendGroup.objects.get(id=group_id))

    def add_friend(self,friend_id):
        self.friendWith.add(Friend.objects.get(id=friend_id))
    
    def remove_friend(self, friend_id):
        self.friendWith.remove(Friend.objects.get(id=friend_id))

    def is_friend(self, friend_id):
        friend = Friend.objects.get(id = friend_id)
        if (friend in self.friendWith.all()):
            return True
        return False


class Location(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    name = models.CharField(
        verbose_name="name", max_length=200, null=True, blank=True)
    address = models.CharField(
        verbose_name="Address", max_length=300, null=True, blank=True)
    phone_number = models.CharField(
        verbose_name="Phone", max_length=100, null=True, blank=True)
    website = models.CharField(
        verbose_name="Website", max_length=1000, null=True, blank=True)
    rating = models.CharField(
        verbose_name="Rating", max_length=40, null=True, blank=True)
    type = models.CharField(
        verbose_name="Type", max_length=100, null=True, blank=True)
    photo_url = models.CharField(
        verbose_name="Photo", max_length=2000, null=True, blank=True)

    longitude = models.CharField(
        verbose_name="Longitude", max_length=50, null=True, blank=True)
    latitude = models.CharField(
        verbose_name="Latitude", max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name


class Calendar(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    visible_for = models.ManyToManyField(User, related_name="visible_for")
    editable_by = models.ManyToManyField(User, related_name="editable_by")

    def __str__(self):
        return self.name

        
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
    creator = models.ForeignKey(Friend, blank=True, on_delete=models.CASCADE)
    attender = models.ManyToManyField(
        Friend, blank=True, related_name='attending_set')
    start_date = models.DateField(null=True)
    start_time = models.TimeField(null=True)
    end_date = models.DateField(null=True)
    end_time = models.TimeField(null=True)
    location = models.ForeignKey(Location, blank=True, on_delete=models.CASCADE,null=True)
    #calendar = models.ForeignKey(Calendar, blank=True, on_delete=models.CASCADE)
    group = models.ForeignKey(FriendGroup, on_delete=models.CASCADE)
    state = models.CharField(
        max_length=2,
        choices=STATE_CHOICES,
        default=PROPOSED,
    )
    ranking = models.IntegerField(null=True, default=0)
    # vote_set for event field in Vote

    def __str__(self):
        return self.name

    def getYeas(self):
        return Vote.objects.filter(event__id=self.id, status=True).count()

    def getNas(self):
        return Vote.objects.filter(event__id=self.id, status=False).count()


class Vote(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    friend = models.ForeignKey(Friend, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.friend}'s vote on {self.event}: {self.status}"


class FriendRequest(models.Model):
    sender = models.ForeignKey(Friend,on_delete=models.DO_NOTHING,related_name='sent_request')
    receiver = models.ForeignKey(Friend,on_delete=models.DO_NOTHING,related_name='received_request')
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender}'s request to {self.receiver}: {self.status}"
