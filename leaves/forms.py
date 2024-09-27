from .models import Leave, Profile
from django.forms import ModelForm
from django import forms
from .models import Profile

class LeaveForm(ModelForm):
    class Meta:
        model = Leave
        fields = ('__all__')
        exclude = ['employee', 'status', 'remarks', 'supervisor']

        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

class ProfileUpdateForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('contact_number', 'email')
        exclude = ('employee',)