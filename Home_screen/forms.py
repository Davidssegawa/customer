from django import forms
from django.forms import DateTimeInput

class DateRangeForm(forms.Form):
    start_timestamp = forms.DateTimeField(label='Start Timestamp', widget=DateTimeInput(attrs={'type': 'datetime-local'}))
    end_timestamp = forms.DateTimeField(label='End Timestamp', widget=DateTimeInput(attrs={'type': 'datetime-local'}))
