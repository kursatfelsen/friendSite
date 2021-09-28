from django.contrib import admin

from .models import FriendGroup, Event, Friend, Vote, Location


admin.site.register(Event)
admin.site.register(Friend)
admin.site.register(Vote)
admin.site.register(Location)

class FriendInline(admin.TabularInline):
    model = Friend.friendGroup.through

@admin.register(FriendGroup)
class FriendGroupAdmin(admin.ModelAdmin):
    model = FriendGroup
    inlines = [
        FriendInline,
    ]
