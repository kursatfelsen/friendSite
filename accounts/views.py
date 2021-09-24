from accounts.forms import UserProfileForm

from core.models import Event, Friend

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User

from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views import View


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


# account/signup/
class SignupView(View):
    """Signup view. Uses UserCrationForm and validates with also ajax in username field. New users should be added as friend too."""

    def render(self, request):
        return render(request, 'signup.html', {'form': self.form})

    def get(self, request, *args, **kwargs):
        self.form = UserCreationForm()
        return self.render(request)

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            Friend.objects.create(user=user)
            return redirect('home')
        messages.error(request, 'Form is invalid')
        self.form = UserCreationForm()
        return self.render(request)


# account/login/
class LoginView(View):
    """Login view."""

    def render(self, request):
        return render(request, 'login.html')

    def get(self, request):
        return self.render(request)

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You logged in successfully.')
            return redirect('profile', username=user.username)
        else:
            messages.warning(
                request, 'Login proccess is not completed properly. Please try again.')
            return self.render(request)


# account/logout
class LogoutView(CustomLoginRequiredMixin, View):
    """Logout View."""
    login_url = 'login'

    def get(self, request):
        messages.error(request, self.permission_denied_message)
        logout(request)
        return redirect('home')


# account/settings/username
class SettingsView(CustomLoginRequiredMixin, View):
    """ Settings view for only to user for editing the account."""

    def render(self, request):
        return render(request, 'settings.html', {'user': self.user, 'friend': self.friend, 'form': self.form, 'groups': self.friendgroups})

    def get(self, request, username):
        self.user = User.objects.get(username=username)
        self.form = UserProfileForm(instance=request.user)
        if request.user.username == self.user.username:
            self.friend = Friend.objects.get(user=self.user)
            self.friendgroups = self.friend.friendGroup.all()
            return self.render(request)
        messages.error(request, "You have no access to that area.")
        return redirect('home')


# account/settings/profile
class ProfileView(CustomLoginRequiredMixin, View):
    """Profile view for everyone."""

    def render(self, request):
        context = {
            'user': self.user,
            'friend': self.friend,
            'groups': self.friendgroups,
            'events_as_creator': self.events_as_creator,
            'events_as_attender': self.events_as_attender
        }
        return render(request, 'profile.html', context)

    def get(self, request, username):
        self.user = User.objects.get(username=username)
        self.friend = Friend.objects.get(user=self.user)
        if request.user == self.user:
            self.friendgroups = self.friend.friendGroup.all()
        else:
            self.friendgroups = self.friend.friendGroup.filter(
                is_private=False)
        self.events_as_creator = Event.objects.filter(creator=self.friend)
        self.events_as_attender = Event.objects.filter(attender=self.friend)
        return self.render(request)


"""For future calendarview purposes"""
# class CalendarView(CustomLoginRequiredMixin, View):
#     def render(self,request):
#         return render(request,'calendar.html')
#     def get(self,request, username):
#         self.user = User.objects.get(username=username)
#         if request.user.username == self.user.username:
#             return self.render(request)
#         messages.error(request, "You have no access to that area.")
#         return redirect('home')


# signup/validate_username/
class ValidateUserNameAjax(View):
    """For Ajax response - Looks for username uniqueness"""

    def get(self, request):
        username = request.GET.get('username')
        data = {
            # case insensitive usernames are used
            'is_taken': User.objects.filter(username__iexact=username).exists()
        }
        if data['is_taken']:
            data['error_message'] = 'A user with this username already exists.'
        return JsonResponse(data)
