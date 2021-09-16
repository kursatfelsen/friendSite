from accounts.forms import UserProfileForm
from core.models import Friend
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.views import View
from django.conf import settings
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



class ProfileView(CustomLoginRequiredMixin,View):
    def render(self,request):
        return render(request,'profile.html',{'user':self.user,'friend':self.friend,'form':self.form,'groups':self.friendgroups})

    def get(self, request, username):
        self.user = User.objects.get(username=username)
        self.form = UserProfileForm(instance=request.user)
        if request.user.username == self.user.username:
            self.friend = Friend.objects.get(user=self.user)
            self.friendgroups = self.friend.friendGroup.all()
            return self.render(request) 
        messages.error(request, "You have no access to that area.")
        return redirect('home')



class CalendarView(CustomLoginRequiredMixin, View):
    def render(self,request):
        return render(request,'calendar.html')
    def get(self,request, username):
        self.user = User.objects.get(username=username)
        if request.user.username == self.user.username:
            return self.render(request)
        messages.error(request, "You have no access to that area.")
        return redirect('home')


def testview(request):
    if request.method == 'POST':
        print(request.POST.get('street_number'))
        print(request.POST.get('county'))
        print(request.POST.get('postal_code'))
        print(request.POST.get('longitude'))
    return render(request,'test.html',{'google_api_key':settings.GOOGLE_API_KEY,'base_country':settings.BASE_COUNTRY})


