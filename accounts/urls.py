from django.urls import path

from .views import *

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('signup/validate_username/',
         ValidateUserNameAjax.as_view(), name='validate_username'),
    path('profile/calendar/<slug:username>/',
         CalendarView.as_view(), name='calendar'),
    path('profile/<slug:username>/', ProfileView.as_view(), name='profile'),
    path('settings/<slug:username>/', SettingsView.as_view(), name='settings'),

    path('add_friend/', SendFriendRequestAjax.as_view(), name='add_friend'),
    path('cancel_request/', CancelRequestAjax.as_view(), name='cancel_request'),
    path('accept_friend/', AcceptFriendAjax.as_view(), name='accept_friend'),
    path('remove/', RemoveFriendAjax.as_view(), name='remove_friend'),
]
