from django import forms
from django.forms.widgets import TimeInput
from django.core.exceptions import ValidationError
from django.db import models
from .models import Event
import datetime

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
            'location_id',
            'location_name',
            'location_address',
            'location_phone_number',
            'location_website',
            'location_rating',
            'location_type',
            'location_photo_url',
            'location_longitude', 
            'location_latitude' ,
            'group',
        ]
        widgets = {
            'start_date': DateInput(attrs={
            'min': datetime.date.today(),
            'max': datetime.date.today()+ datetime.timedelta(days=3650)
            }),
            'end_date': DateInput(attrs={
            'min': datetime.date.today(),
            'max': datetime.date.today()+ datetime.timedelta(days=3650)
            }),
            'start_time': TimeInput(),
            'end_time': TimeInput(),
            'location_id': forms.HiddenInput(attrs={
            'id': 'place_id',
            }),
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
            }) ,
        }
    def clean(self):
        cleaned_data = super().clean()
        print(cleaned_data['start_date'])
        print(cleaned_data['start_date'] > cleaned_data['end_date'])

        if cleaned_data['start_date'] > cleaned_data['end_date']:
            raise ValidationError('End date must be later than start date.')
        if cleaned_data['start_date'] < datetime.datetime.now().date():
            raise ValidationError('Start date must be later than now.')
        

        if cleaned_data['location_name'] == "undefined":
            cleaned_data['location_name'] = ""
        if cleaned_data['location_address'] == "undefined":
            cleaned_data['location_address'] = ""
        if cleaned_data['location_phone_number'] == "undefined":
            cleaned_data['location_phone_number'] = ""
        if cleaned_data['location_website'] == "undefined":
            cleaned_data['location_website'] = ""
        if cleaned_data['location_rating'] == "undefined":
            cleaned_data['location_rating'] = ""
        if cleaned_data['location_type'] == "undefined":
            cleaned_data['location_type'] = ""
        if cleaned_data['location_photo_url'] == "undefined":
            cleaned_data['location_photo_url'] = ""
        return cleaned_data