import heapq

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from safedelete.models import SOFT_DELETE_CASCADE, SafeDeleteModel

from .algorithms import k_means_event

from .managers import *

def calculate_distance(x, y):
    return ((x[0]**2 - y[0]**2) + (x[1]**2 - y[1]**2) + (x[2]**2 - y[2]**2))**(1/3)


class FriendGroup(models.Model):
    name = models.CharField(max_length=50)
    # TODO Wrong foreign key must be friend not user
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    img_url = models.TextField(blank=True)
    is_private = models.BooleanField(default=False)
    # friend_set for friendGroup field in Friend
    # event_set for group field in Event

    def __str__(self):
        return self.name

    def get_friends(self):
        return list(self.friend_set.all())

    def first_upcoming_event(self):
        if self.event_set.all():
            return self.event_set.all()[0]



class Friend(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='friend')
    friendGroup = models.ManyToManyField(FriendGroup, blank=True)
    friendWith = models.ManyToManyField('self', blank=True)
    description = models.TextField(blank=True)
    img = models.TextField(blank=True)
    address = models.CharField(max_length=200, blank=True)
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

    def add_friend(self, friend_id):
        self.friendWith.add(Friend.objects.get(id=friend_id))

    def remove_friend(self, friend_id):
        self.friendWith.remove(Friend.objects.get(id=friend_id))

    def is_friend(self, friend_id):
        friend = Friend.objects.get(id=friend_id)
        if (friend in self.friendWith.all()):
            return True
        return False

    def recommend_event(self):
        event_clusters, kmeans, cluster_labels = k_means_event(self)
        distances = []
        centers = kmeans.cluster_centers_
        if centers == []:
            return
        for friend in self.friendWith.all():
            if len(friend.attending_set.all()) == 0:
                continue
            friend_event_clusters, friend_kmeans, friend_cluster_labels = k_means_event(friend)
            friend_centers = friend_kmeans.cluster_centers_
            if friend_centers == []:
                continue
            for center in centers:
                counter = 0
                for friend_center in friend_centers:
                    distance = calculate_distance(friend_center,center)
                    heapq.heappush(distances, (distance, friend_cluster_labels[counter]))
                    counter += 1

        event_id_set = heapq.heappop(distances)[1]
        return event_id_set
                


class Location(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    name = models.CharField(
        verbose_name='name', max_length=200, blank=True)
    address = models.CharField(
        verbose_name='Address', max_length=300, blank=True)
    phone_number = models.CharField(
        verbose_name='Phone', max_length=100, blank=True)
    website = models.CharField(
        verbose_name='Website', max_length=1000, blank=True)
    rating = models.CharField(
        verbose_name='Rating', max_length=40, blank=True)
    type = models.CharField(
        verbose_name='Type', max_length=100, blank=True)
    photo_url = models.CharField(
        verbose_name='Photo', max_length=2000, blank=True)
    longitude = models.CharField(
        verbose_name='Longitude', max_length=50, blank=True)
    latitude = models.CharField(
        verbose_name='Latitude', max_length=50, blank=True)
    
    def __str__(self):
        return self.name


class Calendar(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    visible_for = models.ManyToManyField(User, related_name='visible_for')
    editable_by = models.ManyToManyField(User, related_name='editable_by')

    def __str__(self):
        return self.name


class Event(models.Model):
    PROPOSED = 'P1'
    PLANNED = 'P2'
    HAPPENING = 'H1'
    HAPPENED = 'H2'
    NOT_HAPPENED = 'N'
    STATE_CHOICES = [
        (PROPOSED, 'Proposed'),
        (PLANNED, 'Planned'),
        (HAPPENING, 'Happening'),
        (HAPPENED, 'Happened'),
        (NOT_HAPPENED, 'Not Happened'),
    ]
    NONE = '0'
    BREAKFAST = '1'
    LUNCH = '2'
    DINNER = '3'
    MEETING = '4'
    ENTERTAINMENT = '5'
    OUTDOOR = '6'
    VACATION = '7'
    WORK = '8'
    STUDY = '9'
    TYPES = [
        (NONE,'None'),
        (BREAKFAST,'Breakfast'),
        (LUNCH,'Lunch'),
        (DINNER,'Dinner'),
        (ENTERTAINMENT,'Entertainment'),
        (WORK,'Work'),
        (MEETING,'Meeting'),
        (OUTDOOR,'Outdoor'),
        (VACATION,'Vacation'),
        (STUDY,'Study'),
    ]

    name = models.CharField(max_length=50)
    description = models.TextField(max_length=2000,blank=True)
    creator = models.ForeignKey(Friend, blank=True, on_delete=models.CASCADE)
    attender = models.ManyToManyField(
        Friend, blank=True, related_name='attending_set')
    start_date = models.DateTimeField(null=True)
    #start_time = models.TimeField(null=True)
    end_date = models.DateTimeField(null=True)
    #end_time = models.TimeField(null=True)
    location = models.ForeignKey(
        Location, blank=True, on_delete=models.CASCADE, null=True)
    #calendar = models.ForeignKey(Calendar, blank=True, on_delete=models.CASCADE)
    group = models.ForeignKey(FriendGroup, on_delete=models.CASCADE)
    state = models.CharField(
        max_length=2,
        choices=STATE_CHOICES,
        default=PROPOSED,
        blank=True
    )
    type = models.CharField(
        max_length=1,
        choices=TYPES,
        default=NONE,
    )
    ranking = models.IntegerField(null=True, default=0)
    # vote_set for event field in Vote
    objects = models.Manager()
    proposed_events = ProposedEventManager()
    planned_events = PlannedEventManager()
    happening_events = HappeningEventManager()
    happened_events = HappenedEventManager()
    not_happened_events = NotHappenedEventManager()

    class Meta:
        ordering = ('state', 'start_date')

    def __str__(self):
        return self.name

    def get_yeah_votes(self):
        return Vote.yeah_votes.filter(event__id=self.id).count()

    def get_nah_votes(self):
        return Vote.nah_votes.filter(event__id=self.id).count()

    def determine_state(self):
        if self.state == 'P2':
            if timezone.now() > self.start_date and timezone.now() < self.end_date:
                self.state = 'H1'
            elif timezone.now() > self.end_date:
                self.state = 'H2'
        elif self.state == 'P1':
            if timezone.now() > self.start_date:
                self.state = 'N'
        self.save()


class EventComment(models.Model):
    creator = models.ForeignKey(Friend, blank=True, on_delete=models.CASCADE)
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(max_length=2000)
    created_time = models.DateTimeField(auto_now_add=True)
    comments = models.ManyToManyField(
        'self', related_name='has_comments', symmetrical=False, blank=True)
    is_inner_comment = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.creator}'s comment on {self.event}"
    

class EventCommentLike(models.Model):
    liker = models.ForeignKey(
        Friend, on_delete=models.CASCADE, related_name='has_comment_likes')
    comment = models.ForeignKey(
        EventComment, on_delete=models.CASCADE, related_name='comment_likes')
    like_or_dislike = models.BooleanField(default=True)

    likes = EventCommentLikeManager()
    

class Vote(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    friend = models.ForeignKey(Friend, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)

    yeah_votes = YeahVoteManager()
    nah_votes = NahVoteManager()
    objects = models.Manager()

    def __str__(self):
        return f"{self.friend}'s vote on {self.event}: {self.status}"


class FriendRequest(models.Model):
    sender = models.ForeignKey(
        Friend, on_delete=models.CASCADE, related_name='sent_request')
    receiver = models.ForeignKey(
        Friend, on_delete=models.CASCADE, related_name='received_request')
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender}'s friend request to {self.receiver}: {self.status}"


class GroupInvitation(models.Model):
    sender = models.ForeignKey(
        Friend, on_delete=models.CASCADE, related_name='sent_invitation')
    receiver = models.ForeignKey(
        Friend, on_delete=models.CASCADE, related_name='received_invitation')
    group = models.ForeignKey(
        FriendGroup, on_delete=models.CASCADE, related_name='invitation_group')
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender}'s group invitation to {self.receiver}: {self.status}"


class Badge(models.Model):
    #owner = models.ForeignKey(Friend, on_delete=models.CASCADE,related_name='badges')
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=200)
    img = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images/', blank=True)

    def __str__(self):
        return self.name


class BadgeFriendRelationship(models.Model):
    owner = models.ForeignKey(
        Friend, on_delete=models.CASCADE, related_name='badge_relation')
    badge = models.ForeignKey(
        Badge, on_delete=models.CASCADE, related_name='owners')

    def __str__(self):
        return f"{self.owner} has {self.badge.name}"


    # def recommend_event(self):
    #     event_clusters, kmeans, cluster_labels = k_means_event(self)
    #     distances = []
    #     centers = kmeans.cluster_centers_
    #     if centers == []:
    #         return
    #     for friend in self.friendWith.all():
    #         if len(friend.attending_set.all()) == 0:
    #             continue
    #         friend_event_clusters, friend_kmeans, friend_cluster_labels = k_means_event(friend)
    #         friend_centers = friend_kmeans.cluster_centers_
    #         if friend_centers == []:
    #             continue
    #         for center in centers:
    #             for friend_center in friend_centers:
    #                 distance = calculate_distance(friend_center,center)
    #                 heapq.heappush(distances, (distance, friend))

    #     value = heapq.heappop(distances)
    #     print(value)