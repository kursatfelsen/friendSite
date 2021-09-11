from django import forms

from .models import Event

class NewEventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'