from datetime import datetime, timedelta
from math import ceil

from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.signing import Signer
from django.db.models import Q
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views import View

from accounts.views import CustomLoginRequiredMixin

from .forms import CalendarForm, LocationForm, NewEventForm, NewGroupForm
from .models import (Badge, BadgeFriendRelationship, Event, EventComment,
                     EventCommentLike, EventCommentLikeManager, Friend,
                     FriendGroup, Location, Vote)

from .algorithms import k_means_event


# /
class HomePageView(View):
    """Web Site's homepage. Friend groups are shown if user is logged in and has groups."""

    def render(self, request):
        if len(self.upcoming_events) >= 1:
            return render(request, 'core/home.html', {'groups': self.groups, 'upcoming_events': self.upcoming_events, 'first_event': self.upcoming_events[0]})
        return render(request, 'core/home.html', {'groups': self.groups, 'upcoming_events': self.upcoming_events})

    def get(self, request):
        if request.user.is_authenticated:
            self.groups = FriendGroup.objects.filter(
                friend=request.user.friend)
            self.upcoming_events = request.user.friend.attending_set.filter(
                state='P2').order_by('start_date')

            return self.render(request)
        else:
            self.groups = []
            return render(request, 'core/home.html')


# group/detail/id
class GroupDetailView(CustomLoginRequiredMixin, View):
    """A friend group's detail view. Friends and events will be rendered for the view. Most of event operations are done here."""

    def render(self, request):
        friends_that_are_not_in_group = Friend.objects.filter(
            Q(friendWith=request.user.friend) & ~Q(friendGroup=self.group))

        try:
            event_accomplishment_rate = len(Event.happened_events.filter(
                group=self.group)) / len(Event.not_happened_events.filter(group=self.group))
        except ZeroDivisionError:
            event_accomplishment_rate = 1
        context = {
            'group': self.group,
            'events': self.first_page_event,
            'all_events': self.all_events,
            'friends_that_are_not_in_group': friends_that_are_not_in_group,
            'page_list_friend': self.page_list,
            'friends': self.first_page,
            'page_list_event': self.page_list_event,
            'event_accomplishment_rate': event_accomplishment_rate,
            'event_objects_type': 'P1',
            'current_page': 1,
        }
        return render(request, 'core/detail.html', context)

    def get(self, request, group_id):
        try:
            self.group = FriendGroup.objects.get(id=group_id)
        except FriendGroup.DoesNotExist:
            messages.error(request, 'No group with that id.')
            return redirect('home')
        friend_objects = Friend.objects.filter(friendGroup__id=group_id)
        paginate_by = 4
        paginator = Paginator(friend_objects, paginate_by)
        page = request.GET.get('page', paginate_by)
        try:
            friends = paginator.page(page)
        except PageNotAnInteger:
            friends = paginator.page(1)
        except EmptyPage:
            friends = paginator.page(paginator.num_pages)
        self.page_list = friends.paginator.page_range
        self.first_page = paginator.page(1).object_list

        event_objects = Event.proposed_events.filter(group=group_id)
        # Update events for they are happening or happened
        for event in event_objects:
            event.determine_state()

        paginate_by_event = 3
        paginator_event = Paginator(event_objects, paginate_by_event)
        page_event = request.GET.get('page', paginate_by_event)
        try:
            events = paginator_event.page(page_event)
        except PageNotAnInteger:
            events = paginator_event.page(1)
        except EmptyPage:
            events = paginator_event.page(paginator_event.num_pages)
        self.page_list_event = range(
            1, ((len(event_objects)+paginate_by-1)//paginate_by)+1)
        self.first_page_event = paginator_event.page(1).object_list
        if (request.user.friend in self.group.get_friends()) or (request.user.friend == self.group.creator):
            self.events = Event.objects.filter(group__id=group_id)
            self.all_events = Event.objects.filter(group__id=group_id)
            return self.render(request)
        self.all_events = Event.objects.filter(group__id=group_id)
        messages.error(request, 'You do not belong to that group')
        return redirect('home')


# group/create/
class GroupCreateView(CustomLoginRequiredMixin, View):
    """Group creation view."""

    def get(self, request):
        self.form = NewGroupForm(
            initial={'creator': request.user.username})
        return render(request, 'core/new_group.html', context={'form': self.form})

    def post(self, request):
        form_data = request.POST.copy()
        form_data['creator'] = request.user.id
        self.form = NewGroupForm(form_data)

        if self.form.is_valid():
            group = self.form.save()
            group.creator = request.user  # Assigning user for security reasons
            request.user.friend.join_group(group.id)  # join group as a friend
            return redirect('detail', group.id)
        messages.error(request, 'Form is invalid')
        return redirect('new_group')


# group/edit/id
class GroupEditView(CustomLoginRequiredMixin, View):
    """Group update view."""

    def render(self, request):
        context = {
            'form': self.form,
            'group': self.group,
        }
        return render(request, 'core/edit_detail.html', context)

    def get(self, request, group_id):
        self.group = FriendGroup.objects.get(id=group_id)
        self.form = NewGroupForm(instance=self.group, initial={
                                 'creator': request.user.username})
        return self.render(request)

    def post(self, request, group_id):
        form_data = request.POST.copy()
        form_data['creator'] = request.user.id
        form = NewGroupForm(form_data)
        print(form)
        if form.is_valid():
            group = FriendGroup.objects.get(id=group_id)
            group.name = form.cleaned_data['name']
            group.img_url = form.cleaned_data['img_url']
            group.is_private = form.cleaned_data['is_private']
            # This should be done here because it can be corrupted in front
            group.creator = request.user
            group.save()
            messages.success(request, 'Successfully updated')
            return redirect('detail', group_id=group.id)
        messages.error(request, 'Form is not valid')
        return redirect('edit_group', group_id=group_id)


# event/newevent/
class NewEventView(CustomLoginRequiredMixin, View):
    """ Event creation view."""

    def render(self, request):
        return render(request, 'core/new_event.html', {'form': self.form})

    def get(self, request):
        friend = request.user.friend
        group_id = request.GET.get('group_id')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        self.form = NewEventForm(
            initial={
                'creator': friend,
                'group': group_id,
                'start_date': start_date,
                'end_date': end_date}
        )
        return self.render(request)

    def post(self, request):
        event_id = request.POST.get('event-id')

        form = NewEventForm(request.POST)
        if form.is_valid():
            event = form.save()
            email_list = []
            for friend in event.group.get_friends():
                email_list.append(friend.user.email)
            send_mail(
            'New Event Created',#Subject
            f'{event.creator} created a new event.Click to see it! http://127.0.0.1:8000/detail/{event.group.id}', #Message
            'kursatfelsen@gmail.com', #from
            email_list, #to
            fail_silently=False,
            )
            try:
                relationship = BadgeFriendRelationship.objects.filter(
                    Q(badge__name='Newbie') & Q(owner__id=event.creator.id))
                if len(relationship) == 0:
                    BadgeFriendRelationship.objects.create(
                        badge=Badge.objects.get(id=3), owner=event.creator)
            except Event.DoesNotExist:
                return redirect('home')
        return redirect('home')


# event/detail/event_id
class EventDetailView(CustomLoginRequiredMixin, View):
    """Event detail view. Event location and attenders will be rendered for view."""

    def render(self, request):
        yeah_votes = Vote.yeah_votes.filter(event=self.event)
        no_votes = Vote.nah_votes.filter(event=self.event)
        comments = EventComment.objects.filter(event=self.event)
        return render(request, 'core/event_detail.html', {'event': self.event, 'yeah_votes': yeah_votes, 'no_votes': no_votes, 'comments': comments})

    def get(self, request, event_id):
        self.event = Event.objects.get(id=event_id)
        return self.render(request)


# event/edit/<int:event_id>
class EventEditView(CustomLoginRequiredMixin, View):
    """Event edit view."""

    def render(self, request):
        context = {
            'form': self.form,
            'event': self.event,
            'location_address': self.location_address,
        }
        return render(request, 'core/edit_event.html', context)

    def get(self, request, event_id):
        self.event = Event.objects.get(id=event_id)
        self.form = NewEventForm(instance=self.event)
        self.location_address = self.event.location_address
        return self.render(request)

    def post(self, request, event_id):
        form = NewEventForm(request.POST)
        if form.is_valid():
            event = Event.objects.get(id=event_id)
            event.name = form.cleaned_data['name']
            event.group = form.cleaned_data['group']
            event.save()
            return redirect('event_detail', event_id=event_id)
        return self.render(request)


# event/delete/event_id
class EventDeleteView(CustomLoginRequiredMixin, View):
    """Event delete view."""

    def render(self, request):
        return render(request, 'core/delete_event.html', {'event': self.event})

    def get(self, request, event_id):
        self.event = Event.objects.get(id=event_id)
        return self.render(request)

    def post(self, request, event_id):
        event = Event.objects.get(id=event_id)
        group_id = event.group.id
        event.delete()
        return redirect('detail', group_id=group_id)


class LocationSetView(CustomLoginRequiredMixin, View):

    def get(self, request, event_id):
        form_location = LocationForm()
        context = {
            'form_location': form_location,
            'event_id': event_id,
        }
        return render(request, 'core/set_location.html', context)

    def post(self, request, event_id):
        try:
            id = request.POST.get('id_id')
            Location.objects.get(id=id)
        except ObjectDoesNotExist:
            self.location_form = LocationForm(request.POST)
            if self.location_form.is_valid():
                location = self.location_form.save()
            else:
                return redirect('location_set', event_id=event_id)

        event = Event.objects.get(id=event_id)
        event.location = location
        event.save()

        return redirect('event_detail', event_id=event.id)


class LocationListView(View):

    def get(self, request):
        locations = Location.objects.all()
        return render(request, 'core/location_list.html', {'location_list': locations})


class LocationDetailView(View):

    def get(self, request, location_id):
        location = Location.objects.get(id=location_id)
        return render(request, 'core/location_detail.html', {'location': location})


class SearchView(View):
    # TODO return only necessary
    def get(self, request):
        search_word = request.GET.get('search_word')
        try:
            events = Event.objects.filter(name__icontains=search_word)
            locations = Location.objects.filter(name__icontains=search_word)
            friends = Friend.objects.filter(
                user__username__icontains=search_word)
            groups = FriendGroup.objects.filter(name__icontains=search_word)
            context = {
                'search_word': search_word,
                'events': events,
                'locations': locations,
                'friends': friends,
                'groups': groups
            }
        except ValueError:
            context = {}
        return render(request, 'core/search_result.html', context)


class JoinEventView(CustomLoginRequiredMixin, View):

    def get(self, request, event_id):
        # P1 and P2 variants
        event = Event.objects.get(id=event_id)
        success_message = 'You have successfuly joined to the event.'
        if event.state == 'P1':
            try:
                # For getting the true vote.
                vote = Vote.objects.get(
                    Q(friend__user__id=request.user.id) & Q(event_id=event_id))
                vote.status = True
            except Vote.DoesNotExist:
                vote = Vote.objects.create(event=Event.objects.get(
                    id=event_id), friend=request.user.friend, status=True)
            vote.save()
            messages.success(request, success_message +
                             'However, this event is not fully planned yet, it can be discarded.')
        elif event.state == 'P2':
            event.attender.add(request.user.friend)
            event.save()
            messages.success(request, success_message)
        else:
            messages.error(
                request, 'You can not join an event that is already happened.')
        return redirect('event_detail', event_id=event_id)


class RecommendEventView(CustomLoginRequiredMixin, View):

    def get(self, request):
        event_ids = request.user.friend.recommend_event()
        event_list = []
        for id in event_ids:
            event_list.append(Event.objects.get(id=id))
        return render(request, 'core/event_recommendations.html', {'event_list': event_list})


# vote/
class VoteAjax(CustomLoginRequiredMixin, View):
    """For Ajax response - Handles voting system for events."""

    def get(self, request):
        user_id = request.GET.get('user_id', None)
        event_id = request.GET.get('event_id', None)
        status = request.GET.get('status', None)
        is_render = request.GET.get('render', None)
        event = Event.objects.get(id=event_id)
        if is_render:  # Just render the corresponding field
            context = {
                'yeah_votes': Vote.yeah_votes.filter(event=event),
                'no_votes': Vote.nah_votes.filter(event=event)
            }
            return render(request, 'core/ajax_render/event_voters.html', context)

        if status == '0':
            status = False
        elif status == '1':
            status = True
        else:  # Vote cancellation status is 2.
            Vote.objects.filter(Q(event_id=event_id) &
                                Q(friend__user__id=user_id)).delete()
            data = {'result': True}
            return JsonResponse(data)
        try:
            # For getting the true vote.
            vote = Vote.objects.get(
                Q(friend__user__id=user_id) & Q(event_id=event_id))
            vote.status = status
        except Vote.DoesNotExist:
            vote = Vote.objects.create(event=Event.objects.get(
                id=event_id), friend=request.user.friend, status=status)

        vote.save()

        data = {
            'yeas': event.get_yeah_votes(),
            'nas': event.get_nah_votes(),
        }
        return JsonResponse(data)


# dismiss/
class DismissAjax(CustomLoginRequiredMixin, View):
    """For Ajax response - Handles dismissing friends for groups."""

    def get(self, request):
        user_id = request.GET.get('user_id', None)
        group_id = request.GET.get('group_id', None)
        friend = Friend.objects.get(user__id=user_id)
        try:
            friend.leave_group(group_id)
            data = {
                'dismissed': True,
                'name': friend.user.username,
            }
        except:
            data = {
                'dismissed': False
            }
        return JsonResponse(data)


# add/
class AddUserToGroupAjax(CustomLoginRequiredMixin, View):
    """For Ajax response - Handles adding friends for groups."""

    def get(self, request):
        user_id = request.GET.get('user_id', None)
        group_id = request.GET.get('group_id', None)
        friend = Friend.objects.get(user__id=user_id)
        try:
            friend.join_group(group_id)
            data = {
                'added': True,
                'name': friend.user.username,
            }
        except:
            data = {
                'added': False
            }
        return JsonResponse(data)


# plan/
class PlanAjax(CustomLoginRequiredMixin, View):
    """For Ajax response - Handles changing event's state from P1(proposed) to P2(Planned).Adds yeah voted users as attenders."""

    def get(self, request):
        event_id = request.GET.get('event_id', None)
        event = Event.objects.get(id=event_id)
        if event.creator.user.id == request.user.id:
            event.state = 'P2'
            votes = Vote.objects.filter(event__id=event_id, status=True)
            for i in votes:
                event.attender.add(i.friend)
            event.save()
            # TODO send email or notification to accepted friends
            data = {
                'planned': True,
                'event_name': event.name,
                'attenders': list(event.attender.all().values_list('user__username')),
            }
            return JsonResponse(data)
        data = {
            'planned': False
        }
        return JsonResponse(data)


# paginate/
class UserPaginateAjax(View):
    """For Ajax response - Handles user pagination"""

    def get(self, request):
        page = int(request.GET.get('page', None))
        group = request.GET.get('group', None)
        paginate_by = 4
        starting_number = (page-1)*paginate_by
        ending_number = page*paginate_by
        friends_all = list(Friend.objects.filter(friendGroup__id=group))
        friends = friends_all[starting_number:ending_number]
        page_list_friend = range(
            1, ((len(friends_all)+paginate_by-1)//paginate_by)+1)
        return render(request, 'core/ajax_render/user_pagination.html', {'friends': friends, 'page_list_friend': page_list_friend, 'current_page': page})


# eventpaginate/
class EventPaginateAjax(View):
    """For Ajax response - Handles event pagination"""

    def get(self, request):
        page = int(request.GET.get('page', None))
        group = request.GET.get('group', None)
        event_type = request.GET.get('event_type', None)
        paginate_by = 3
        starting_number = (page-1)*paginate_by
        ending_number = page*paginate_by
        if event_type == 'P1':
            events_all = list(Event.proposed_events.filter(group__id=group))
        elif event_type == 'P2':
            events_all = list(Event.planned_events.filter(group__id=group))
        elif event_type == 'H1':
            events_all = list(Event.happening_events.filter(group__id=group))
        elif event_type == 'H2':
            events_all = list(Event.happened_events.filter(group__id=group))
        elif event_type == 'N':
            events_all = list(
                Event.not_happened_events.filter(group__id=group))
        else:
            return render(request, 'core/ajax_render/event_pagination.html',)
        events = events_all[starting_number:ending_number]
        page_list_event = range(
            1, ((len(events_all)+paginate_by-1)//paginate_by)+1)
        return render(request, 'core/ajax_render/event_pagination.html', {'events': events, 'event_objects_type': event_type, 'page_list_event': page_list_event, 'current_page': page})


# submit/
class SubmitEventFormAjax(View):
    """For Ajax response - Handles form submission"""

    def post(self, request):
        form = NewEventForm(request.POST)
        if form.is_valid():
            event = form.save()
            form_location = LocationForm()
            return render(request, 'core/ajax_render/map_form.html', context={'form_location': form_location, 'event_id': event.id})


class EventCommentCreateAjax(View):

    def get(self, request):
        comment_content = request.GET.get('content', None)
        event_id = request.GET.get('event_id', None)
        is_inner = request.GET.get('inner_comment', None)
        event = Event.objects.get(id=event_id)
        if is_inner == '0':
            outer_comment_id = request.GET.get('outer_comment_id', None)
            outer_comment = EventComment.objects.get(id=outer_comment_id)
            comment = EventComment.objects.create(
                creator=request.user.friend,
                event=event,
                content=comment_content,
                is_inner_comment=True,
            )
            outer_comment.comments.add(comment)
            outer_comment.save()
        else:
            EventComment.objects.create(
                creator=request.user.friend,
                event=event,
                content=comment_content,
            )
        return render(request, 'core/ajax_render/comments.html', context={'comments': event.comments.all()})


class LikeEventCommentAjax(View):
    def get(self, request):
        comment_id = request.GET.get('comment_id', None)
        event_id = request.GET.get('event_id', None)
        status = request.GET.get('status', None)
        event = Event.objects.get(id=event_id)
        comment = EventComment.objects.get(id=comment_id)
        try:
            event_comment_like = EventCommentLike.likes.filter(
                Q(comment=comment) & Q(liker=request.user.friend))[0]
            if status == 'false':
                if event_comment_like.like_or_dislike == False:
                    event_comment_like.delete()
                else:
                    event_comment_like.like_or_dislike = False
                    event_comment_like.save()
            else:
                if event_comment_like.like_or_dislike == True:
                    event_comment_like.delete()
                else:
                    event_comment_like.like_or_dislike = True
                    event_comment_like.save()

        except IndexError:
            if status == 'false':
                EventCommentLike.likes.create(
                    liker=request.user.friend, comment=comment, like_or_dislike=False)
            else:
                EventCommentLike.likes.create(
                    liker=request.user.friend, comment=comment, like_or_dislike=True)

        return render(request, 'core/ajax_render/comments.html', context={'comments': event.comments.all()})


class TestView(View):

    def get(self, request, group_id):
        length = int(request.GET.get('length'))
        length_for_pause = int(request.GET.get('length_for_pause'))
        friends = Friend.objects.filter(friendGroup__id=group_id)
        #exclude = [23,7]
        starting_time_to_try = timezone.now() + timedelta(hours=length_for_pause) + \
            timedelta(hours=3)  # Last timedelta is for correcting timezone
        ending_time_to_try = starting_time_to_try + timedelta(hours=length)
        full_list = []
        while(True):
            flag = False
            for friend in friends:
                for attending_event in friend.attending_set.all():
                    # engaged time contains the interval in it
                    if starting_time_to_try > attending_event.start_date and ending_time_to_try < attending_event.end_date:
                        flag = True
                        starting_time_to_try = attending_event.end_date + \
                            timedelta(hours=length_for_pause)
                        ending_time_to_try = starting_time_to_try + \
                            timedelta(hours=length)
                        break
                    elif starting_time_to_try < attending_event.start_date and ending_time_to_try > attending_event.end_date:  # event contains engaged time
                        flag = True
                        starting_time_to_try = attending_event.end_date + \
                            timedelta(hours=length_for_pause)
                        ending_time_to_try = starting_time_to_try + \
                            timedelta(hours=length)
                        break
                    elif starting_time_to_try < attending_event.end_date and ending_time_to_try > attending_event.start_date:  # event start time is in engaged time
                        flag = True
                        starting_time_to_try = attending_event.end_date + \
                            timedelta(hours=length_for_pause)
                        ending_time_to_try = starting_time_to_try + \
                            timedelta(hours=length)
                        break
                    elif starting_time_to_try < attending_event.end_date and ending_time_to_try > attending_event.start_date:  # event end time is in engaged time
                        flag = True
                        starting_time_to_try = attending_event.end_date + \
                            timedelta(hours=length_for_pause)
                        ending_time_to_try = starting_time_to_try + \
                            timedelta(hours=length)
                        break
                if starting_time_to_try.hour == 23:
                    starting_time_to_try += timedelta(hours=8)
                elif starting_time_to_try.hour == 6:
                    starting_time_to_try += timedelta(hours=1)
                elif starting_time_to_try.hour == 5:
                    starting_time_to_try += timedelta(hours=2)
                elif starting_time_to_try.hour == 4:
                    starting_time_to_try += timedelta(hours=3)
                elif starting_time_to_try.hour == 3:
                    starting_time_to_try += timedelta(hours=4)
                elif starting_time_to_try.hour == 2:
                    starting_time_to_try += timedelta(hours=5)
                elif starting_time_to_try.hour == 1:
                    starting_time_to_try += timedelta(hours=6)
                elif starting_time_to_try.hour == 0:
                    starting_time_to_try += timedelta(hours=7)
                ending_time_to_try = starting_time_to_try + \
                    timedelta(hours=length)
            if flag:
                flag = False
                # Only look for 1 days ahead
                if starting_time_to_try > (timezone.now() + timedelta(days=15)):
                    print('There is no possible interval.')
                    context = {
                        'error': 'There is no possible interval in your group schedule.'
                    }
                    break
            else:
                starting_time_formatted = starting_time_to_try.strftime(
                    '%Y-%m-%dT%H:%M')
                ending_time_formatted = ending_time_to_try.strftime(
                    '%Y-%m-%dT%H:%M')
                full_list.append(
                    [starting_time_formatted, ending_time_formatted])
                starting_time_to_try += timedelta(hours=1)
                ending_time_to_try += timedelta(hours=1)
                # print
                # (f'FOUND IT:{starting_time_to_try}-{ending_time_to_try}')
                # context = {
                #     'start_time': starting_time_to_try,
                #     'end_time': ending_time_to_try,
                # }
        context = {
            'full_list': full_list[:10],
            'group_id': group_id,
        }
        return render(request, 'core/event_finder.html', context)
