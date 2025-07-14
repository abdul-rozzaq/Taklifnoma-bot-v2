from django import forms

from .models import Event


class EventSelectForm(forms.Form):
    event = forms.ModelChoiceField(queryset=Event.objects.all(), label="Tadbirni tanlang")
