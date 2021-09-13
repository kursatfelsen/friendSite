from django import forms

from .models import Event

class DateInput(forms.DateInput):
    input_type = 'date'
    

class NewEventForm(forms.ModelForm):
    
    class Meta:
        model = Event
        fields = ['name', 'start_date','end_date','location','group']
        widgets = {
            'start_date': DateInput(),
            'end_date': DateInput(),
        }
