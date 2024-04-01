from django import forms
from django.forms import DateTimeInput
from .models import WaterUnit


class DateRangeForm(forms.Form):
    start_timestamp = forms.DateTimeField(label='start_timestamp', widget=DateTimeInput(attrs={'type': 'datetime-local'}))
    end_timestamp = forms.DateTimeField(label='end_timestamp', widget=DateTimeInput(attrs={'type': 'datetime-local'}))



# class PurchaseForm(forms.Form):
#     unit = forms.ModelChoiceField(queryset=WaterUnit.objects.all(), empty_label=None)
#     phone_number = forms.CharField(max_length=15)  # Or use a PhoneField if available in your Django version

class PurchaseForm(forms.Form):
    UNIT_CHOICES = [
        (unit.id, f"{unit.name} - Ugx{unit.price}") for unit in WaterUnit.objects.all()
    ]
    unit = forms.ChoiceField(choices=UNIT_CHOICES,widget=forms.RadioSelect)
    phone_number = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'placeholder': 'Enter your phone number', 'required': True}))
