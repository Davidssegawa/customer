
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
from .models import Meter_data 
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import MeterDataSerializer
import json
from django.utils import timezone
import plotly.express as px
from .forms import DateRangeForm
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

@csrf_exempt
def ttn_webhook(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        print(data)

        timestamp = timezone.now()

        text = data.get("uplink_message",{}).get('decoded_payload',{}).get('text')

        print("Text:",text)
        print("Timestamp:",timestamp)

        meter_data = Meter_data(timestamp=timestamp,text=text)
        meter_data.save()


        return JsonResponse({'message': 'Data received and saved.'})
    else:
        return JsonResponse({'error':'Invalid request method.'}, status=405)
    
class MeterDataList(APIView):
    def get(self):
        meter_data = Meter_data.objects.all()
        serializer = MeterDataSerializer(meter_data, many=True)
        return Response(serializer.data)
    

def chart_view(request):
    form = DateRangeForm(request.GET or None)  # Initialize the form instance
    
    # Retrieve all Meter_data objects from the database
    meter_data = Meter_data.objects.all()

    if form.is_valid():
        start_timestamp = form.cleaned_data.get('start_timestamp')
        end_timestamp = form.cleaned_data.get('end_timestamp')

        if start_timestamp:
            meter_data = meter_data.filter(timestamp__gte=start_timestamp)
        if end_timestamp:
            meter_data = meter_data.filter(timestamp__lte=end_timestamp)
    data = {
        'Timestamp': [data.timestamp for data in meter_data],
        'Water Measurements': [data.text for data in meter_data]  # Assuming 'value' is the field containing water measurements
    }

    # Create a DataFrame from the data dictionary
    df = pd.DataFrame(data)

    # Create the line chart
    fig = px.line(df, x='Timestamp', y='Water Measurements', title="Real-time water usage")
    # Prepare data for the line chart
    # fig = px.line(
    #     df,
    #     x='Timestamp',
    #     y='Water Measurements',
    #     title="Real-time water usage",
    #     labels={'x': 'Timestamp', 'y': 'Water measurements'}
    # )

    chart_html = fig.to_html(full_html=False)
    context = {'chart_html': chart_html, "form": form}
    return render(request, 'sections/Statistics.html', context)