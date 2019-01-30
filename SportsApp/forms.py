from django import forms
from .models import MatchEvent


class AddEventForm(forms.ModelForm):
    class Meta:
        model = MatchEvent
        fields = ('title', 'comment')
