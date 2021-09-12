from django import forms

from .models import Event

class DateInput(forms.DateInput):
    input_type = 'date'
    

class NewEventForm(forms.ModelForm):
    
    class Meta:
        model = Event
        fields = ['name', 'date', 'location','group']
        widgets = {
            'date': DateInput(),
        }