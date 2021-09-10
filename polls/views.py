from django.http.response import HttpResponse
from django.shortcuts import render


from django.views import View
from .models import Question
# Create your views here.

class PollListView(View):
    def render(self,request):
        return render(request,'polls.html',{'polls':self.polls})

    def get(self, request):
        self.polls = Question.objects.all()
        self.render(request)


def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)