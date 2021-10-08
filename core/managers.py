from django.db import models


class FriendGroupManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class FriendManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class LocationManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class EventManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class EventCommentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class VoteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class EventCommentLikeManager(models.Manager):
    def total_likes(self):
        return len(self.get_queryset().filter(like_or_dislike=True)) - len(self.get_queryset().filter(like_or_dislike=False))
