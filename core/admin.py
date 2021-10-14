from django.contrib import admin

from .models import (Badge, BadgeFriendRelationship, Event,
                     EventComment, EventCommentLike, Friend, FriendGroup,
                     FriendRequest, GroupInvitation, Location, Vote)

admin.site.register(EventCommentLike)


class EventCommentInline(admin.TabularInline):
    model = EventComment


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'creator', 'start_date',
                    'end_date', 'type', 'location', 'group', 'state')
    inlines = [
        EventCommentInline,
    ]


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('event', 'friend', 'status')


class EventInline(admin.TabularInline):
    model = Event.attender.through


@admin.register(Friend)
class VoteAdmin(admin.ModelAdmin):
    model = Friend
    inlines = [
        EventInline,
    ]

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'type')


class FriendInline(admin.TabularInline):
    model = Friend.friendGroup.through


@admin.register(FriendGroup)
class FriendGroupAdmin(admin.ModelAdmin):
    model = FriendGroup
    inlines = [
        FriendInline,
    ]


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


@admin.register(BadgeFriendRelationship)
class BadgeFriendRelationshipAdmin(admin.ModelAdmin):
    list_display = ('owner', 'badge')


@admin.register(FriendRequest)
class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver')


@admin.register(GroupInvitation)
class GroupInvitationAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'group')


@admin.register(EventComment)
class EventCommentAdmin(admin.ModelAdmin):
    list_display = ('creator', 'event', 'created_time')
