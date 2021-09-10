from django.http.response import HttpResponse
from django.shortcuts import render
from django.views import View
# Create your views here.

from .models import FriendGroup

class HomePageView(View):
    def render(self, request):
        return render(request, 'home.html', {'groups': self.groups})

    def get(self, request, *args, **kwargs):
        self.groups = FriendGroup.objects.all()
        return self.render(request)

class GroupDetailView(View):
    def render(self, request):
        return render(request,'detail.html',{'group':self.group})

    def get(self, request, group_id):
        self.group = FriendGroup.objects.get(id = group_id)
        return self.render(request)