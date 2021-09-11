from django.urls import path

from .views import HomePageView, GroupDetailView, NewEventView

urlpatterns = [
    path('', HomePageView.as_view(),name='home'),
    path('detail/<int:group_id>/', GroupDetailView.as_view(),name='detail'),
    path('newevent/',NewEventView.as_view(), name='new_event')
]