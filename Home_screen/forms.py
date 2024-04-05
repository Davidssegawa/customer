from django import forms
from django.forms import DateTimeInput
from .models import WaterUnit
import requests

class DateRangeForm(forms.Form):
    start_timestamp = forms.DateTimeField(label='start_timestamp', widget=DateTimeInput(attrs={'type': 'datetime-local'}))
    end_timestamp = forms.DateTimeField(label='end_timestamp', widget=DateTimeInput(attrs={'type': 'datetime-local'}))



# class PurchaseForm(forms.Form):
#     unit = forms.ModelChoiceField(queryset=WaterUnit.objects.all(), empty_label=None)
#     phone_number = forms.CharField(max_length=15)  # Or use a PhoneField if available in your Django version




class PurchaseForm(forms.Form):
    unit = forms.ChoiceField(widget=forms.RadioSelect)
    phone_number = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'placeholder': 'Enter your phone number', 'required': True}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Make API call to fetch WaterUnit data
        api_url = 'https://fyp-4.onrender.com/api/waterunits/'  # Adjust the API URL
        response = requests.get(api_url)
        if response.status_code == 200:
            water_units = response.json()
            choices = [(unit['id'], f"{unit['name']} - Ugx{unit['price']}") for unit in water_units]
            self.fields['unit'].choices = choices
        else:
            # Handle API error
            self.fields['unit'].choices = []
