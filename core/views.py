from django.contrib.auth.models import User
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.views import View

from .models import Vote

# Create your views here.

from .forms import NewEventForm
from .models import Event, Friend, FriendGroup

class HomePageView(View):
    def render(self, request):
        return render(request, 'home.html', {'groups': self.groups})

    def get(self, request, *args, **kwargs):
        try:
            self.groups = FriendGroup.objects.filter(friend = Friend.objects.get(user__id = request.user.id))
        except Friend.DoesNotExist:
            self.groups = []
        return self.render(request)

class GroupDetailView(View):
    def render(self, request):
        users = User.objects.all()
        return render(request,'detail.html',{'group':self.group,'events':self.events,'users':users})

    def get(self, request, group_id):
        self.group = FriendGroup.objects.get(id = group_id)
        self.events = Event.objects.filter(group__id=group_id)
        return self.render(request)

    def post(self,request,group_id):
        new_user = request.POST['new_user']
        Friend.objects.get(user__id=new_user).friendGroup.add(FriendGroup.objects.get(id=group_id))
        return redirect('detail',group_id=group_id)



class NewEventView(View):
    def render(self, request):
        return render(request,'new_event.html',{'form':self.form})

    def get(self, request):
        self.form = NewEventForm
        return self.render(request)

    def post(self, request):
        self.form = NewEventForm(request.POST)
        if self.form.is_valid():
            event = self.form.save()
            return  redirect('event_detail',event.id)
        return self.render(request)


class EventDetailView(View):
    def render(self, request):
        return render(request,'event_detail.html',{'event':self.event})

    def get(self, request, event_id):
        self.event = Event.objects.get(id = event_id)
        return self.render(request)


class EventEditView(View):
    def render(self, request):
        return render(request,'edit_event.html',{'form':self.form,'event':self.event})

    def get(self, request, event_id):
        self.event = Event.objects.get(id=event_id)
        self.form = NewEventForm(instance=self.event)
        return self.render(request)

    def post(self, request,event_id):
        form = NewEventForm(request.POST)
        if form.is_valid():
            event = Event.objects.get(id=event_id)
            event.name = form.cleaned_data['name']
            event.date = form.cleaned_data['date']
            event.location = form.cleaned_data['location']
            event.group = form.cleaned_data['group']
            event.save()
            return redirect('event_detail',event_id=event_id)
        return self.render(request)


class EventDeleteView(View):
    def render(self, request):
        return render(request,'delete_event.html',{'event':self.event})

    def get(self,request,event_id):
        self.event = Event.objects.get(id=event_id)
        return self.render(request)

    def post(self,request, event_id):
        event = Event.objects.get(id=event_id)
        group_id = event.group.id
        event.delete()
        return redirect('detail',group_id=group_id)


def vote(request, group_id, event_id, status):
    friend = Friend.objects.get(user__id = request.user.id)
    friend_id = friend.id
    if status == 0:
        status = False
    else:
        status = True
    Vote.objects.filter(event_id=event_id, friend__id = friend_id).delete()
    Vote.objects.create(friend_id=friend_id,event_id=event_id,status=status)
    return redirect('detail',group_id = group_id)

