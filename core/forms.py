import datetime

from django import forms

from django.forms.widgets import TimeInput
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User

from .models import Calendar, Event, FriendGroup, Location



class DateInput(forms.DateInput):
    input_type = 'date'


class TimeInput(forms.TimeInput):
    input_type = 'time'


class NewEventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'name',
            'start_date',
            'start_time',
            'end_date',
            'end_time',
            'location',
            'group',
            'creator',
        ]
        widgets = {
            'start_date': DateInput(attrs={
                'min': datetime.date.today(),
                'max': datetime.date.today() + datetime.timedelta(days=3650)
            }),
            'end_date': DateInput(attrs={
                'min': datetime.date.today(),
                'max': datetime.date.today() + datetime.timedelta(days=3650)
            }),
            'start_time': TimeInput(),
            'end_time': TimeInput(),
            'location': forms.HiddenInput(attrs={
                'id': 'place_id',
            }),
            'creator': forms.HiddenInput(attrs={
                'id': 'creator',
            }),
            'group': forms.HiddenInput(attrs={
                'id': 'group',
            }),
        }

    def clean(self):
        cleaned_data = super().clean()

        #Protection against old date input
        if cleaned_data['start_date'] > cleaned_data['end_date']:
            raise ValidationError('End date must be later than start date.')
        if cleaned_data['start_date'] < datetime.datetime.now().date():
            raise ValidationError('Start date must be later than now.')


class NewGroupForm(forms.ModelForm):
    class Meta:
        model = FriendGroup
        fields = '__all__'
        widgets = {
            'creator': forms.TextInput(attrs={ #This field is not for taking input, just for giving info to user
                'readonly': "readonly",
                'id':'creator',
            })}


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = '__all__'
        widgets = {
            'location_name': forms.HiddenInput(attrs={
                'id': 'name',
            }),
            'location_address': forms.HiddenInput(attrs={
                'id': 'formatted_address',
            }),
            'location_phone_number': forms.HiddenInput(attrs={
                'id': 'formatted_phone_number',
            }),
            'location_website': forms.HiddenInput(attrs={
                'id': 'website',
            }),
            'location_rating': forms.HiddenInput(attrs={
                'id': 'rating',
            }),
            'location_type': forms.HiddenInput(attrs={
                'id': 'type',
            }),
            'location_photo_url': forms.HiddenInput(attrs={
                'id': 'photo',
            }),
            'location_longitude': forms.HiddenInput(attrs={
                'id': 'longtitude',
            }),
            'location_latitude': forms.HiddenInput(attrs={
                'id': 'latitude',
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        #Google places api undefined data fields should be empty.
        cleaned_data['type'] = cleaned_data['type'].replace('_',' ')
        if cleaned_data['name'] == "undefined":
            cleaned_data['name'] = ""
        if cleaned_data['address'] == "undefined":
            cleaned_data['address'] = ""
        if cleaned_data['phone_number'] == "undefined":
            cleaned_data['phone_number'] = ""
        if cleaned_data['website'] == "undefined":
            cleaned_data['website'] = ""
        if cleaned_data['rating'] == "undefined":
            cleaned_data['rating'] = ""
        if cleaned_data['type'] == "undefined":
            cleaned_data['type'] = ""
        if cleaned_data['photo_url'] == "undefined":
            cleaned_data['photo_url'] = ""
        return cleaned_data


class CalendarForm(forms.ModelForm):
    visible_for = forms.CharField(required=False)
    editable_by = forms.CharField(required=False)

    class Meta:
        model = Calendar
        exclude = ("owner","visible_for","editable_by")

    def save(self, commit=True):
        calendar = self.instance
        for email in self.cleaned_data["visible_for"].split(";"):
            if User.objects.filter(email=email).exists():
                calendar.visible_for.add(email)
        for email in self.cleaned_data["editable_by"].split(";"):
            if User.objects.filter(email=email).exists():
                calendar.editable_by.add(email)
        if commit:
            calendar.save()
        return calendar

# class EventForm(forms.ModelForm):
#     class Meta:
#         model = Event
#         exclude = ()