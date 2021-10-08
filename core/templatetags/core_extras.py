from django import template
from django.db.models.query_utils import Q
from core.models import *
register = template.Library()


@register.simple_tag
def is_liked(comment_id, friend_id):
    friend = Friend.objects.get(id=friend_id)
    comment = EventComment.objects.get(id=comment_id)
    try:
        comment_like = EventCommentLike.likes.filter(
            Q(liker=friend) & Q(comment=comment))[0]
        if comment_like.like_or_dislike == True:
            return "color:red;"
        else:
            return ""
    except EventComment.DoesNotExist:
        return ""
    except IndexError:
        return ""


@register.simple_tag
def is_disliked(comment_id, friend_id):
    friend = Friend.objects.get(id=friend_id)
    comment = EventComment.objects.get(id=comment_id)
    try:
        comment_like = EventCommentLike.likes.filter(
            Q(liker=friend) & Q(comment=comment))[0]
        if comment_like.like_or_dislike == False:
            return "color:blue;"
        else:
            return ""
    except EventComment.DoesNotExist:
        return ""
    except IndexError:
        return ""
