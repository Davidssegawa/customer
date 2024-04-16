
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import CreateView
import pandas as pd
#from .models import Meter_data 
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
#from .serializers import MeterDataSerializer
import json
from django.utils import timezone
import plotly.express as px
from .forms import DateRangeForm
#from .models import WaterUnit
#from .forms import PurchaseForm
import requests
from django import forms
import random
import string
import requests
from django.shortcuts import render, redirect
from .forms import PrepaymentOptionForm
from .pay import PayClass



def index(request):
    return render(request,'authentication/index.html')



def signin(request):

    if request.method == "POST":
        username = request.POST['username']
        pass1 = request.POST['pass1']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request,'User does not exist')

        user = authenticate(request,username=username, password=pass1)

        if user is not None:
            login(request,user)
            return redirect('home')

        else:
            messages.error(request, 'Wrong credentials')
            return redirect('index')   
         
    return render(request,'authentication/signin.html')

@login_required(login_url='signin')
def home(request):
    return render(request, 'authentication/home.html')

def signout(request):
    logout(request)
    messages.success(request, "Logged out!")
    return redirect("index")

'''@login_required(login_url='signin')
def map(request):
    return render(request,'sections/Map.html')'''

@login_required(login_url='signin')
def statistics(request):
    return render(request,'sections/Statistics.html')


@login_required(login_url='signin')
def payment(request):
    return render(request,'sections/Payment.html')

@login_required(login_url='signin')
def purchase_confirmation(request):
    return render(request,'sections/purchase_confirmation.html')

# def buy_water(request):
#     if request.method == 'POST':
#         form = PurchaseForm(request.POST)
#         if form.is_valid():
#             unit_id = form.cleaned_data['unit_id']
#             phone_number = form.cleaned_data['phone_number']
            
#             # Make API call to fetch WaterUnit data
#             api_url = 'https://fyp-4.onrender.com/api/waterunits/'.format(unit_id)  # Adjust the API URL
#             response = requests.get(api_url)
#             if response.status_code == 200:
#                 unit_data = response.json()
#                 unit_price = unit_data.get('price')  # Assuming the API response contains price information
#             else:
#                 # Handle API error
#                 unit_price = None  # Set unit price to None if API call fails
            
#             if unit_price is not None:
#                 # Process payment with MOMO API (example using requests library)
#                 momo_api_url = 'MOMO_API_URL'  # Replace with the actual URL of the MOMO API endpoint
#                 momo_response = requests.post(momo_api_url, data={'unit_id': unit_id, 'phone_number': phone_number, 'amount': unit_price})
#                 if momo_response.status_code == 200:  # Assuming successful payment
#                     return redirect('purchase_confirmation', unit_id=unit_id)
#                 else:
#                     # Handle payment failure
#                     pass
#     else:
#         form = PurchaseForm()
#     return render(request, 'sections/Payment.html', {'form': form})

# def purchase_confirmation(request, unit_id):
#     # Here you can directly use the unit_id to display confirmation
#     return render(request, 'sections/purchase_confirmation.html', {'unit_id': unit_id})



#fetching meter data from the postgreSQL and then plotting the chart
def chart_view(request):
    form = DateRangeForm(request.GET or None)

    # Make API call to the second project to fetch meter data
    api_url = 'https://fyp-4.onrender.com/api/meter-data/'  # Replace with actual API URL
    response = requests.get(api_url)
    if response.status_code == 200:
        meter_data = response.json()
    else:
        meter_data = []  # Empty list if API call fails

    if form.is_valid():
        start_timestamp = form.cleaned_data.get('start_timestamp')
        end_timestamp = form.cleaned_data.get('end_timestamp')

        # Filter data based on date range if provided
        if start_timestamp:
            meter_data = meter_data.filter(timestamp__gte=start_timestamp)
        if end_timestamp:
            meter_data = meter_data.filter(timestamp__lte=end_timestamp)
    data = {
        'Timestamp': [data['timestamp'] for data in meter_data],
        'Water Measurements': [data['text'] for data in meter_data]  # Assuming 'value' is the field containing water measurements
    }
    # Create a DataFrame from the retrieved meter data
    df = pd.DataFrame(data)

    # Create the line chart
    fig = px.line(df, x='Timestamp', y='Water Measurements', title="Real-time water usage")

    # Convert the plot to HTML
    chart_html = fig.to_html(full_html=False)
    
    context = {'chart_html': chart_html, "form": form}
    return render(request, 'sections/Statistics.html', context)



#PAYMENT OPTIONS 
#OPTION 1: NO API

def prepayment(request):
    # Fetch prepayment options from FYP_server's API
    response = requests.get('https://fyp-4.onrender.com/api/prepayment-options/')
    if response.status_code == 200:
        options_data = response.json()
        options = [(option['id'], f"{option['name']}, (UGx{option['price']})") for option in options_data]
    else:
        # If request fails, set options to an empty list
        options = []
    # Define choices for selected_option field
    #selected_option = forms.ChoiceField(choices=options, widget=forms.RadioSelect)

    if request.method == 'POST':
        form = PrepaymentOptionForm(request.POST)
        form.fields['selected_option'].choices = options
        print("form",form)
        if form.is_valid():
            selected_option_id = form.cleaned_data['selected_option']
            # Generate confirmation code
            confirmation_code = f"{selected_option_id}-{''.join(random.choices(string.ascii_uppercase + string.digits, k=6))}"
            print("confirmation code",confirmation_code)
            # Send transaction details to FYP_server's API
            transaction_data = {'selected_option': selected_option_id, 'confirmation_code': confirmation_code, "option_id":selected_option_id}
            transaction_response = requests.post('https://fyp-4.onrender.com/api/transactions/', data=transaction_data)
            if transaction_response.status_code == 201:
                transaction_id = transaction_response.json()['id']
                print(transaction_id)
                return redirect('purchase_confirmation', transaction_id=transaction_id)
            else:
                # Handle error when transaction is not found
                return render(request, 'sections/purchase_confirmation_error.html')
    else:
        form = PrepaymentOptionForm()
        form.fields['selected_option'].choices =options

    return render(request, 'sections/Payment.html', {'form': form})

# def payment_confirmation(request, transaction_id):
#     # Fetch transaction details from the first project's API
#     transaction_response = requests.get(f'https://fyp-4.onrender.com/api/transactions/{transaction_id}/')
#     if transaction_response.status_code == 200:
#         transaction_data = transaction_response.json()
#         transaction = {
#             'option_name': transaction_data['option']['name'],
#             'confirmation_code': transaction_data['confirmation_code'],
#             'option_id':transaction_data['option_id']
#         }
#         return render(request, 'sections/purchase_confirmation.html', {'transaction': transaction})
#     else:
#         # Handle error when transaction is not found
#         return render(request, 'sections/purchase_confirmation_error.html')

#OPTION 2: MOMO_API
# def prepayment(request):
#     # Fetch prepayment options from FYP_server's API
#     response = requests.get('https://fyp-4.onrender.com/api/prepayment-options/')
#     if response.status_code == 200:
#         options_data = response.json()
#         options = [(option['id'], f"{option['name']}, (UGx{option['price']})") for option in options_data]
#     else:
#         # If request fails, set options to an empty list
#         options = []

#     if request.method == 'POST':
#         form = PrepaymentOptionForm(request.POST)
#         form.fields['selected_option'].choices = options
#         if form.is_valid():
#             selected_option_id = form.cleaned_data['selected_option']
#             phone_number = form.cleaned_data['phone_number']  # Retrieve the phone number from the form
#             # Generate confirmation code
#             confirmation_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
#             # Send transaction details to FYP_server's API
#             transaction_data = {'selected_option': selected_option_id, 'confirmation_code': confirmation_code}
#             transaction_response = requests.post('https://fyp-4.onrender.com/api/transactions/', data=transaction_data)
#             if transaction_response.status_code == 201:
#                 transaction_id = transaction_response.json()['id']
#                 #return redirect('payment_confirmation', transaction_id=transaction_id)
                
#                 # Initialize MOMO API class
#                 momo_api = PayClass()
                
#                 # Perform MOMO payment
#                 momo_response = momo_api.momopay(form.cleaned_data['selected_option'][1], "EUR", transaction_id, phone_number, "Water payment")
#                 print(momo_response["response"])
#                 print(momo_response["ref"])
#                 verify = momo_api.verifymomo(momo_response["ref"])
#                 print(verify)
#                 if momo_response["response"] == 202:  # Assuming successful payment
#                     return HttpResponse(confirmation_code)  # Return the confirmation code as plain text
#                 else:
#                     # Handle payment failure
#                     pass
#     else:
#         form = PrepaymentOptionForm()
#         form.fields['selected_option'].choices = options

#     return render(request, 'sections/Payment.html', {'form': form})

# def payment_confirmation(request, transaction_id):
#     # Fetch transaction details from the first project's API
#     transaction_response = requests.get(f'https://fyp-4.onrender.com/api/transactions/{transaction_id}/')
#     if transaction_response.status_code == 200:
#         transaction_data = transaction_response.json()
#         transaction = {
#             'option_name': transaction_data['option']['name'],
#             'confirmation_code': transaction_data['confirmation_code'],
#         }
#         return render(request, 'sections/purchase_confirmation.html', {'transaction': transaction})
#     else:
#         # Handle error when transaction is not found
#         return render(request, 'sections/purchase_confirmation_error.html')


#OPTION 3: STRIPE API

'''import stripe
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import PrepaymentOptionForm
import random
import string

def prepayment(request):
    # Fetch prepayment options from FYP_server's API
    response = requests.get('https://fyp-4.onrender.com/api/prepayment-options/')
    if response.status_code == 200:
        options_data = response.json()
        options = [(option['id'], f"{option['name']}, (UGx{option['price']})") for option in options_data]
    else:
        # If request fails, set options to an empty list
        options = []

    if request.method == 'POST':
        form = PrepaymentOptionForm(request.POST)
        form.fields['selected_option'].choices = options
        if form.is_valid():
            selected_option_id = form.cleaned_data['selected_option']
            #phone_number = form.cleaned_data['phone_number']  # Retrieve the phone number from the form
            # Generate confirmation code
            confirmation_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            # Send transaction details to FYP_server's API
            transaction_data = {'selected_option': selected_option_id, 'confirmation_code': confirmation_code}
            transaction_response = requests.post('https://fyp-4.onrender.com/api/transactions/', data=transaction_data)
            if transaction_response.status_code == 201:
                transaction_id = transaction_response.json()['id']
                # Initialize Stripe API
                stripe.api_key = settings.STRIPE_SECRET_KEY
                
                # Create a Stripe PaymentIntent
                payment_intent = stripe.PaymentIntent.create(
                    amount=form.cleaned_data['selected_option'][1] * 100,  # Convert amount to cents
                    currency='eur',
                    description='Water payment',
                    #receipt_email=phone_number,
                    payment_method_types=['card'],
                    metadata={'transaction_id': transaction_id}
                )
                
                if payment_intent.status == 'requires_action':  
                    # The payment requires additional actions, handle it according to the next action
                    return HttpResponse(payment_intent.next_action)
                elif payment_intent.status == 'succeeded':
                    # Payment succeeded, return the confirmation code
                    return render(request, 'purchase_confirmation.html', {'confirmation_code': confirmation_code})
                else:
                    # Handle payment failure
                    pass
    else:
        form = PrepaymentOptionForm()
        form.fields['selected_option'].choices = options

    return render(request, 'sections/Payment.html', {'form': form})'''
