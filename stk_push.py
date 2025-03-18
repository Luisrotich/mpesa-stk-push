import requests
import os
import base64
from dotenv import load_dotenv
from datetime import datetime
from get_access_token import get_access_token

# Load environment variables
load_dotenv()

# Get credentials from .env
business_shortcode = os.getenv("BUSINESS_SHORTCODE")
passkey = os.getenv("PASSKEY")
callback_url = os.getenv("CALLBACK_URL")

def generate_password():
    """Generate the Lipa Na M-Pesa Online password."""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    data_to_encode = business_shortcode + passkey + timestamp
    encoded_password = base64.b64encode(data_to_encode.encode()).decode('utf-8')
    return encoded_password, timestamp

def stk_push(phone_number, amount):
    """Initiate an STK Push request."""
    access_token = get_access_token()
    if not access_token:
        print("Failed to get access token")
        return

    password, timestamp = generate_password()

    url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    
    payload = {
        "BusinessShortCode": business_shortcode,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone_number,
        "PartyB": business_shortcode,
        "PhoneNumber": phone_number,
        "CallBackURL": callback_url,
        "AccountReference": "Test Payment",
        "TransactionDesc": "Payment for goods"
    }

    print("Sending STK Push Request to Safaricom...")
    print("Payload:", payload)  # Debugging


    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        print("STK Push sent successfully!")
        print(response.json())
    else:
        print("Error:", response.status_code, response.text)

if __name__ == "__main__":
    phone_number = input("Enter phone number (e.g. 2547XXXXXXXX): ")
    amount = input("Enter amount: ")
    stk_push(phone_number, amount)
