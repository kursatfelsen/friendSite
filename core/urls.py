from django.urls import path

from .views import *

urlpatterns = [
    # Home
    path('', HomePageView.as_view(), name='home'),

    # Group
    path('group/create/', GroupCreateView.as_view(), name='new_group'),
    path('group/detail/<int:group_id>/',
         GroupDetailView.as_view(), name='detail'),
    path('group/edit/<int:group_id>/',
         GroupEditView.as_view(), name='edit_group'),

    # Event
    path('event/newevent/', NewEventView.as_view(), name='new_event_post'),
    path('event/newevent/',
         NewEventView.as_view(), name='new_event_get'),
    path('event/detail/<int:event_id>',
         EventDetailView.as_view(), name='event_detail'),
    path('event/edit/<int:event_id>', EventEditView.as_view(), name='event_edit'),
    path('event/delete/<int:event_id>',
         EventDeleteView.as_view(), name='event_delete'),
    path('event/join/<int:event_id>', JoinEventView.as_view(), name='event_join'),

    # Location
    path('location/', LocationListView.as_view(), name='location_list'),
    path('location/<int:event_id>/',LocationSetView.as_view(),name='location_set'),
    path('location/<slug:location_id>/',
         LocationDetailView.as_view(), name='location_detail'),
    
    # Search
    path('search/', SearchView.as_view(), name='search'),

    # Recommend
    path('recommend/', RecommendEventView.as_view(), name='recommend_event'),

    # Ajax
    path('dismiss/', DismissAjax.as_view(), name='dismiss'),
    path('vote/', VoteAjax.as_view(), name='vote'),
    path('add/', AddUserToGroupAjax.as_view(), name='addUserToGroup'),
    path('plan/', PlanAjax.as_view(), name='plan'),
    path('paginate/', UserPaginateAjax.as_view(), name='paginate'),
    path('eventpaginate/', EventPaginateAjax.as_view(), name='paginate_event'),
    path('submit/', SubmitEventFormAjax.as_view(), name='submit_event'),
    path('event/comment/', EventCommentCreateAjax.as_view(), name='create_comment'),
    path('event/comment/like', LikeEventCommentAjax.as_view(), name='like_comment'),

    path('test/<int:group_id>/', TestView.as_view(), name='test')
]
