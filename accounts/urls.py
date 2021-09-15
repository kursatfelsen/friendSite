from django.urls import path

from .views import *

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/',LoginView.as_view(), name='login'),
    path('logout/',LogoutView.as_view(), name='logout'),
    path('profile/<slug:username>/',ProfileView.as_view(), name='profile'),
    path('profile/<slug:username>/calendar/',CalendarView.as_view(), name='calendar'),
    path('test',testview,name='test'),
]