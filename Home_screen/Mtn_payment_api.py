# views.py
import requests
from django.conf import settings
from django.http import HttpResponse

def initiate_payment(request):
    # Retrieve payment details from request, e.g., amount, phone number, etc.
    amount = request.POST.get('amount')
    phone_number = request.POST.get('phone_number')
    
    # Construct payment request payload
    payload = {
        'amount': amount,
        'phoneNumber': phone_number,
        'apiKey': settings.MTN_API_KEY,
        'apiSecret': settings.MTN_API_SECRET,
        'callbackUrl': settings.MTN_CALLBACK_URL,
    }
    
    # Make HTTP request to MTN Uganda's payment endpoint
    response = requests.post(settings.MTN_PAYMENT_ENDPOINT, json=payload)
    
    # Process response from MTN Uganda
    if response.status_code == 200:
        # Payment initiated successfully
        payment_data = response.json()
        payment_id = payment_data.get('paymentId')
        return HttpResponse(f'Payment initiated successfully. Payment ID: {payment_id}')
    else:
        # Error handling
        error_message = response.text
        return HttpResponse(f'Failed to initiate payment. Error: {error_message}', status=response.status_code)

def handle_payment_callback(request):
    # Process payment callback from MTN Uganda
    # Extract payment status and other details from callback payload
    # Update payment status in your database or perform other actions as needed
    return HttpResponse(status=200)  # Respond with HTTP 200 OK to acknowledge callback
