from django.urls import path

from .views import *

urlpatterns = [
    #Home
    path('', HomePageView.as_view(),name='home'),

    #Group
    path('group/create/',GroupCreateView.as_view(), name='new_group'),
    path('group/detail/<int:group_id>/', GroupDetailView.as_view(),name='detail'),
    path('group/edit/<int:group_id>/',GroupEditView.as_view(), name='edit_group'),

    #Event
    path('event/newevent/',NewEventView.as_view(), name='new_event_post'),
    path('event/newevent/<int:group_id>',NewEventView.as_view(), name='new_event_get'),
    path('event/detail/<int:event_id>',EventDetailView.as_view(),name='event_detail'),
    path('event/edit/<int:event_id>',EventEditView.as_view(),name = 'event_edit'),
    path('event/delete/<int:event_id>',EventDeleteView.as_view(),name='event_delete'),

    #Ajax
    path('dismiss/',DismissAjax.as_view(),name='dismiss'),
    path('vote/',VoteAjax.as_view(),name='vote'),
    path('add/',AddUserToGroupAjax.as_view(),name='addUserToGroup'),
    path('plan/',PlanAjax.as_view(),name='plan'),
    path('paginate/',UserPaginateAjax.as_view(),name='paginate'),
]