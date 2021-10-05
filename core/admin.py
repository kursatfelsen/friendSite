from django.contrib import admin

from .models import FriendGroup, Event, Friend, FriendRequest, Vote, Location, Calendar, GroupInvitation


admin.site.register(Event)
admin.site.register(Friend)
admin.site.register(Vote)
admin.site.register(Location)
admin.site.register(Calendar)
admin.site.register(FriendRequest)
admin.site.register(GroupInvitation)

class FriendInline(admin.TabularInline):
    model = Friend.friendGroup.through

@admin.register(FriendGroup)
class FriendGroupAdmin(admin.ModelAdmin):
    model = FriendGroup
    inlines = [
        FriendInline,
    ]
