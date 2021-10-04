from django.contrib import messages
from django.core.signing import Signer
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.views import View

from accounts.views import CustomLoginRequiredMixin

from .forms import CalendarForm, LocationForm, NewEventForm, NewGroupForm, LocationForm
from .models import Event, Friend, FriendGroup, Vote


# /
class HomePageView(View):
    """Web Site's homepage. Friend groups are shown if user is logged in and have groups."""

    def render(self, request):
        return render(request, 'core/home.html', {'groups': self.groups})

    def get(self, request):
        if request.user.is_authenticated:
            self.groups = FriendGroup.objects.filter(
                friend=request.user.friend.get())
            return self.render(request)
        else:
            self.groups = []
            return self.render(request)


# group/detail/id
class GroupDetailView(CustomLoginRequiredMixin, View):
    """A friend group's detail view. Friends and events will be rendered for the view. Most of event operations are done here."""

    def render(self, request):
        friends_that_are_not_in_group = Friend.objects.filter(
            Q(friendWith=request.user.friend.get()) & ~Q(friendGroup=self.group))
        context = {
            'group': self.group,
            'events': self.first_page_event,
            'friends': friends_that_are_not_in_group,
            'page_list': self.page_list,
            'page': self.first_page,
            'page_list_event': self.page_list_event,
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

        event_objects = Event.objects.filter(group=group_id)
        paginate_by_event = 3
        paginator_event = Paginator(event_objects, paginate_by_event)
        page_event = request.GET.get('page', paginate_by_event)
        try:
            events = paginator_event.page(page_event)
        except PageNotAnInteger:
            events = paginator_event.page(1)
        except EmptyPage:
            events = paginator_event.page(paginator_event.num_pages)
        self.page_list_event = paginator_event.page_range
        self.first_page_event = paginator_event.page(1).object_list
        if (request.user.friend.get() in self.group.get_friends()) or (request.user.friend.get() == self.group.creator):
            self.events = Event.objects.filter(group__id=group_id)
            return self.render(request)

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
        formData =  request.POST.copy()
        formData['creator'] = request.user.id
        self.form = NewGroupForm(formData)
        
        if self.form.is_valid():
            group = self.form.save()
            group.creator = request.user  # Assigning user for security reasons
            request.user.friend.get().join_group(group.id)  # join group as a friend
            return redirect('detail', group.id)
        messages.error(request, 'Form is invalid')
        return redirect('new_group')


# group/edit/id
class GroupEditView(CustomLoginRequiredMixin, View):
    """"Group update view."""

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
        form = NewGroupForm(request.POST)
        if form.is_valid():
            group = FriendGroup.objects.get(id=group_id)
            group.name = form.cleaned_data['name']
            group.img_url = form.cleaned_data['img_url']
            group.is_private = form.cleaned_data['is_private']
            # This should be done here because it can be corrupted in front
            group.creator = request.user
            group.save()
            return redirect('detail', group_id=group.id)
        messages.error(request, 'Form is not valid')
        return redirect('edit_group', group_id=group_id)


# event/newevent/
class NewEventView(CustomLoginRequiredMixin, View):
    """ Event creation view."""

    def render(self, request):
        return render(request, 'core/new_event.html', {'form': self.form})

    def get(self, request, group_id):
        friend = request.user.friend.get()
        self.form = NewEventForm(
            initial={'creator': friend, 'group': group_id})
        return self.render(request)

    def post(self, request):
        event_id = request.POST.get('event-id')
        self.location_form = LocationForm(request.POST)
        print(self.location_form)
        if self.location_form.is_valid():
            location = self.location_form.save()
            event = Event.objects.get(id = event_id)
            event.location = location
            event.save()
            return redirect('home')
        return redirect('home')

# event/detail/event_id


class EventDetailView(CustomLoginRequiredMixin, View):
    """Event detail view. Event location and attenders will be rendered for view."""

    def render(self, request):
        return render(request, 'core/event_detail.html', {'event': self.event})

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


# vote/
class VoteAjax(CustomLoginRequiredMixin, View):
    """For Ajax response - Handles voting system for events."""

    def get(self, request):
        user_id = request.GET.get('user_id', None)
        event_id = request.GET.get('event_id', None)
        status = request.GET.get('status', None)

        if status == "0":
            status = False
        elif status == "1":
            status = True
        else:  # Vote cancellation status is 2.
            Vote.objects.filter(event_id=event_id,
                                friend__user__id=user_id).delete()
            data = {'result': True}
            return JsonResponse(data)
        try:
            # For getting the true vote.
            vote = Vote.objects.get(
                Q(friend__user__id=user_id) & Q(event_id=event_id))
            vote.status = status
        except Vote.DoesNotExist:
            vote = Vote.objects.create(event=Event.objects.get(
                id=event_id), friend=request.user.friend.get(), status=status)

        vote.save()
        event = Event.objects.get(id=event_id)
        data = {
            'yeas': event.getYeas(),
            'nas': event.getNas(),
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
        starting_number = (page-1)*4
        ending_number = page*4
        friends = list(Friend.objects.filter(friendGroup__id=group)[
            starting_number:ending_number])
        return render(request, 'core/ajax_render/user_pagination.html', {'page': friends})


# eventpaginate/
class EventPaginateAjax(View):
    """For Ajax response - Handles event pagination"""

    def get(self, request):
        page = int(request.GET.get('page', None))
        group = request.GET.get('group', None)
        starting_number = (page-1)*3
        ending_number = page*3
        events = list(Event.objects.filter(group__id=group)[
            starting_number:ending_number])
        return render(request, 'core/ajax_render/event_pagination.html', {'events': events})


# submit/
class SubmitEventFormAjax(View):
    """For Ajax response - Handles form submission"""

    def post(self, request):
        form = NewEventForm(request.POST)
        if form.is_valid():
            event = form.save()
            form_location = LocationForm()
            return render(request,'core/ajax_render/map_form.html',context={'form_location':form_location,'event_id':event.id})

