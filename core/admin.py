from django.contrib import admin

from .models import EventCommentLike, EventComment, FriendGroup, Event, Friend, FriendRequest, Vote, Location, Calendar, GroupInvitation, Badge, BadgeFriendRelationship


admin.site.register(Friend)
admin.site.register(EventCommentLike)

class EventCommentInline(admin.TabularInline):
    model = EventComment

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'creator', 'start_date',
                    'end_date', 'location', 'group', 'state')
    inlines = [
        EventCommentInline,
    ]


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('event', 'friend', 'status')


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