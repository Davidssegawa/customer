from django import forms
from django.forms import DateTimeInput
#from .models import WaterUnit
import requests
# from .models import PrepaymentOption


class DateRangeForm(forms.Form):
    start_timestamp = forms.DateTimeField(label='start_timestamp', widget=DateTimeInput(attrs={'type': 'datetime-local'}))
    end_timestamp = forms.DateTimeField(label='end_timestamp', widget=DateTimeInput(attrs={'type': 'datetime-local'}))



# class PurchaseForm(forms.Form):
#     unit = forms.ModelChoiceField(queryset=WaterUnit.objects.all(), empty_label=None)
#     phone_number = forms.CharField(max_length=15)  # Or use a PhoneField if available in your Django version

# 



class PrepaymentOptionForm(forms.Form):
    # Fetch prepayment options from FYP_server's API
    response = requests.get('https://fyp-4.onrender.com/api/prepayment-options/')
    if response.status_code == 200:
        options_data = response.json()
        options = [(option['id'], f"{option['name']},(UGx{option['price']}") for option in options_data]
    else:
        # If request fails, set options to an empty list
        options = []

    # Define choices for selected_option field
    selected_option = forms.ChoiceField(choices=options, widget=forms.RadioSelect)
