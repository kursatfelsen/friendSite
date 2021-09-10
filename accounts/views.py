from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.views import View

# Create your views here.

class SignupView(View):
    def render(self,request):
        return render(request, 'signup.html', {'form': self.form})
    
    def get(self,request,*args,**kwargs):
        self.form = UserCreationForm()
        return self.render(request)