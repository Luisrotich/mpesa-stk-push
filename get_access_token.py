import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get credentials from .env
consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET")

def get_access_token():
    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(url, auth=(consumer_key, consumer_secret))
    
    if response.status_code == 200:
        token = response.json()["access_token"]
        return token
    else:
        return None

if __name__ == "__main__":
    access_token = get_access_token()
    print("Access Token:", access_token)
