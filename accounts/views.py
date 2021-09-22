from accounts.forms import UserProfileForm
from core.models import Event, Friend, FriendGroup
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.views import View
from django.conf import settings
from django.http import JsonResponse
# Create your views here.


class SignupView(View):
    def render(self,request):
        return render(request, 'signup.html', {'form': self.form})
    
    def get(self,request,*args,**kwargs):
        self.form = UserCreationForm()
        return self.render(request)

    def post(self,request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            Friend.objects.create(user=user)
            return redirect('home')
        messages.error(request,'Form is invalid')
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



class SettingsView(CustomLoginRequiredMixin,View):
    def render(self,request):
        return render(request,'settings.html',{'user':self.user,'friend':self.friend,'form':self.form,'groups':self.friendgroups})

    def get(self, request, username):
        self.user = User.objects.get(username=username)
        self.form = UserProfileForm(instance=request.user)
        if request.user.username == self.user.username:
            self.friend = Friend.objects.get(user=self.user)
            self.friendgroups = self.friend.friendGroup.all()
            return self.render(request) 
        messages.error(request, "You have no access to that area.")
        return redirect('home')


class ProfileView(CustomLoginRequiredMixin,View):
    #Change here
    def render(self,request):
        return render(request,'profile.html',{'user':self.user,'friend':self.friend,'groups':self.friendgroups,'events_as_creator':self.events_as_creator,'events_as_attender':self.events_as_attender})

    def get(self, request, username):
        self.user = User.objects.get(username=username)
        self.friend = Friend.objects.get(user=self.user)
        self.friendgroups = self.friend.friendGroup.all()
        self.events_as_creator = Event.objects.filter(creator=self.friend)
        self.events_as_attender = Event.objects.filter(attender=self.friend)
        return self.render(request) 


class CalendarView(CustomLoginRequiredMixin, View):
    def render(self,request):
        return render(request,'calendar.html')
    def get(self,request, username):
        self.user = User.objects.get(username=username)
        if request.user.username == self.user.username:
            return self.render(request)
        messages.error(request, "You have no access to that area.")
        return redirect('home')


class ValidateUserNameAjax(View):
    def get(self,request):
        username = request.GET.get('username', None)
        data = {
            'is_taken': User.objects.filter(username__iexact=username).exists()
        }
        if data['is_taken']:
            data['error_message'] = 'A user with this username already exists.'
        return JsonResponse(data)
