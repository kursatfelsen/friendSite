from django.urls import path

from .views import *

urlpatterns = [
    path('', HomePageView.as_view(),name='home'),
    path('detail/<int:group_id>/', GroupDetailView.as_view(),name='detail'),
    path('event/newevent/',NewEventView.as_view(), name='new_event'),
    path('event/detail/<int:event_id>',EventDetailView.as_view(),name='event_detail'),
    path('event/edit/<int:event_id>',EventEditView.as_view(),name = 'event_edit'),
    path('event/delete/<int:event_id>',EventDeleteView.as_view(),name='event_delete'),
    path('detail/<int:group_id>/vote/<int:event_id>/<int:status>', VoteView.as_view(),name='vote'),
    path('detail/<int:group_id>/dismiss/<int:user_id>',DismissView.as_view(),name='dismiss'),
]