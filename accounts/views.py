from core.models import Friend
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.views import View

# Create your views here.

class SignupView(View):
    def render(self,request):
        return render(request, 'signup.html', {'form': self.form})
    
    def get(self,request,*args,**kwargs):
        self.form = UserCreationForm()
        return self.render(request)



class LoginView(View):
    def render(self,request):
        return render(request,'login.html')

    def get(self, request):
        return self.render(request)

    def post(self,request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You logged in successfully.')
            return redirect('profile', username=user.username)
        else:
            messages.warning(request, 'Login proccess is not completed properly. Please try again.')
            return self.render(request)


class CustomLoginRequiredMixin(LoginRequiredMixin):
    """ The LoginRequiredMixin extended to add a relevant message to the
    messages framework by setting the ``permission_denied_message``
    attribute. """
    permission_denied_message = 'You have to be logged in to access that page'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.add_message(request, messages.WARNING,
                                self.permission_denied_message)
            return self.handle_no_permission()
        return super(CustomLoginRequiredMixin, self).dispatch(
            request, *args, **kwargs
        )

class LogoutView(CustomLoginRequiredMixin,View):
    login_url = 'login'
    def get(self,request):
        messages.error(request,self.permission_denied_message)
        logout(request)
        return redirect('home')



class ProfileView(CustomLoginRequiredMixin,View):
    def render(self,request):
        return render(request,'profile.html',{'user':self.user,'friend':self.friend})

    def get(self, request, username):
        self.user = User.objects.get(username=username)
        self.friend = Friend.objects.get(user=self.user)
        return self.render(request)