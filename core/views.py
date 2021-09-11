from django.http.response import HttpResponse
from django.shortcuts import render
from django.views import View
# Create your views here.

from .forms import NewEventForm
from .models import Event, FriendGroup

class HomePageView(View):
    def render(self, request):
        return render(request, 'home.html', {'groups': self.groups})

    def get(self, request, *args, **kwargs):
        self.groups = FriendGroup.objects.all()
        return self.render(request)

class GroupDetailView(View):
    def render(self, request):
        return render(request,'detail.html',{'group':self.group,'events':self.events})

    def get(self, request, group_id):
        self.group = FriendGroup.objects.get(id = group_id)
        self.events = Event.objects.filter(group__id=group_id)
        return self.render(request)


class NewEventView(View):
    def render(self, request):
        return render(request,'new_event.html',{'form':self.form})

    def get(self, request):
        self.form = NewEventForm
        return self.render(request)

    def post(self, request):
        self.form = NewEventForm(request.POST)
        if self.form.is_valid():
            self.form.save()
            return self.render(request)
        return self.render(request)