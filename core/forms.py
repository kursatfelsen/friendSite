from django import forms

from .models import Event

class DateInput(forms.DateInput):
    input_type = 'date'
    

class NewEventForm(forms.ModelForm):
    
    class Meta:
        model = Event
        fields = [
            'name', 
            'start_date','end_date',
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
            'start_date': DateInput(),
            'end_date': DateInput(),
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