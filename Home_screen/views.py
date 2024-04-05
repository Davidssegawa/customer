
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
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
#from .serializers import MeterDataSerializer
import json
from django.utils import timezone
import plotly.express as px
from .forms import DateRangeForm
#from .models import WaterUnit
from .forms import PurchaseForm
import requests


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

# @csrf_exempt
# def ttn_webhook(request):
#     if request.method == 'POST':
#         data = json.loads(request.body.decode('utf-8'))
#         print(data)

#         timestamp = timezone.now()

#         text = data.get("uplink_message",{}).get('decoded_payload',{}).get('text')

#         print("Text:",text)
#         print("Timestamp:",timestamp)

#         meter_data = Meter_data(timestamp=timestamp,text=text)
#         meter_data.save()


#         return JsonResponse({'message': 'Data received and saved.'})
#     else:
#         return JsonResponse({'error':'Invalid request method.'}, status=405)
    
# class MeterDataList(APIView):
#     def get(self):
#         meter_data = Meter_data.objects.all()
#         serializer = MeterDataSerializer(meter_data, many=True)
#         return Response(serializer.data)
    

# def chart_view(request):
#     form = DateRangeForm(request.GET or None)  # Initialize the form instance
    
#     # Retrieve all Meter_data objects from the database
#     meter_data = Meter_data.objects.all()

#     if form.is_valid():
#         start_timestamp = form.cleaned_data.get('start_timestamp')
#         end_timestamp = form.cleaned_data.get('end_timestamp')

#         if start_timestamp:
#             meter_data = meter_data.filter(timestamp__gte=start_timestamp)
#         if end_timestamp:
#             meter_data = meter_data.filter(timestamp__lte=end_timestamp)
#     data = {
#         'Timestamp': [data.timestamp for data in meter_data],
#         'Water Measurements': [data.text for data in meter_data]  # Assuming 'value' is the field containing water measurements
#     }

#     # Create a DataFrame from the data dictionary
#     df = pd.DataFrame(data)

#     # Create the line chart
#     fig = px.line(df, x='Timestamp', y='Water Measurements', title="Real-time water usage")
#     # Prepare data for the line chart
#     # fig = px.line(
#     #     df,
#     #     x='Timestamp',
#     #     y='Water Measurements',
#     #     title="Real-time water usage",
#     #     labels={'x': 'Timestamp', 'y': 'Water measurements'}
#     # )

#     chart_html = fig.to_html(full_html=False)
#     context = {'chart_html': chart_html, "form": form}
#     return render(request, 'sections/Statistics.html', context)


import requests

def buy_water(request):
    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        if form.is_valid():
            unit_id = form.cleaned_data['unit_id']
            phone_number = form.cleaned_data['phone_number']
            
            # Make API call to fetch WaterUnit data
            api_url = 'https://fyp-4.onrender.com/api/waterunits/'.format(unit_id)  # Adjust the API URL
            response = requests.get(api_url)
            if response.status_code == 200:
                unit_data = response.json()
                unit_price = unit_data.get('price')  # Assuming the API response contains price information
            else:
                # Handle API error
                unit_price = None  # Set unit price to None if API call fails
            
            if unit_price is not None:
                # Process payment with MOMO API (example using requests library)
                momo_api_url = 'MOMO_API_URL'  # Replace with the actual URL of the MOMO API endpoint
                momo_response = requests.post(momo_api_url, data={'unit_id': unit_id, 'phone_number': phone_number, 'amount': unit_price})
                if momo_response.status_code == 200:  # Assuming successful payment
                    return redirect('purchase_confirmation', unit_id=unit_id)
                else:
                    # Handle payment failure
                    pass
    else:
        form = PurchaseForm()
    return render(request, 'sections/Payment.html', {'form': form})

def purchase_confirmation(request, unit_id):
    # Here you can directly use the unit_id to display confirmation
    return render(request, 'sections/purchase_confirmation.html', {'unit_id': unit_id})



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
    fig = px.line(df, x='timestamp', y='Water Measurements', title="Real-time water usage")

    # Convert the plot to HTML
    chart_html = fig.to_html(full_html=False)
    
    context = {'chart_html': chart_html, "form": form}
    return render(request, 'sections/Statistics.html', context)
