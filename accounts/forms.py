from django import forms
from django.contrib.auth.models import User
from core.models import Friend


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
        ]
        widgets = {
            'email': forms.EmailInput(attrs={
                'id': 'email',
            }),
        }

class FriendProfileForm(forms.ModelForm):
    class Meta:
        model = Friend
        fields = [
            'description',
            'img',
            'address',
            'phone',
        ]
        widgets = {
            'description': forms.TextInput(attrs={
                'id': 'description',
            }),
            'img': forms.TextInput(attrs={
                'id': 'img',
            }),
            'address': forms.TextInput(attrs={
                'id': 'address',
            }),
        }