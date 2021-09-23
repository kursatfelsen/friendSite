from django.urls import path

from .views import *

urlpatterns = [
    path('login/',LoginView.as_view(), name='login'),
    path('logout/',LogoutView.as_view(), name='logout'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('signup/validate_username/',ValidateUserNameAjax.as_view(), name='validate_username'),
    #path('profile/calendar/<slug:username>/',CalendarView.as_view(), name='calendar'), Will be used.
    path('profile/<slug:username>/',ProfileView.as_view(), name='profile'),
    path('settings/<slug:username>/',SettingsView.as_view(), name='settings'),
]