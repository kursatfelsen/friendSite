from django.db import models


class SoftDeleteManager(models.Manager):
    """Use this manager to get objects that have a deleted field"""

    def get_queryset(self):
        return super(SoftDeleteManager, self).get_queryset().filter(deleted=False)

    def all_with_deleted(self):
        return super(SoftDeleteManager, self).get_queryset()

    def deleted_set(self):
        return super(SoftDeleteManager, self).get_queryset().filter(deleted=True)


class YeahVoteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status = True)


class NahVoteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status = False)


class EventCommentLikeManager(models.Manager):
    def total_likes(self):
        return len(self.get_queryset().filter(like_or_dislike=True)) - len(self.get_queryset().filter(like_or_dislike=False))


class ProposedEventManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(state='P1')


class PlannedEventManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(state='P2')


class HappeningEventManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(state='H1')


class HappenedEventManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(state='H2')


class NotHappenedEventManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(state='N')
