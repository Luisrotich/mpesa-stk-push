# app.py
from flask import Flask, render_template, request, jsonify
import requests
import base64
from datetime import datetime

app = Flask(__name__)

# M-Pesa API Credentials
BUSINESS_SHORTCODE = "174379"
PASSKEY = "your_passkey_here"
CONSUMER_KEY = "your_consumer_key_here"
CONSUMER_SECRET = "your_consumer_secret_here"
CALLBACK_URL = "https://your-callback-url.com"

# Get M-Pesa Access Token
def get_access_token():
    url = "https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(url, auth=(CONSUMER_KEY, CONSUMER_SECRET))
    return response.json().get("access_token")

# Route: Home (Products Page)
@app.route("/")
def home():
    return render_template("products.html")

# Route: Payment Page
@app.route("/payment")
def payment():
    product = request.args.get("product")
    price = request.args.get("price")
    return render_template("payment.html", product=product, price=price)

# Route: STK Push (Trigger Payment)
@app.route("/stkpush", methods=["POST"])
def stkpush():
    data = request.json
    phone = data["phone"]
    amount = data["amount"]

    access_token = get_access_token()
    if not access_token:
        return jsonify({"error": "Failed to get access token"}), 500

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    password = base64.b64encode((BUSINESS_SHORTCODE + PASSKEY + timestamp).encode()).decode()

    stk_push_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    payload = {
        "BusinessShortCode": BUSINESS_SHORTCODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone,
        "PartyB": BUSINESS_SHORTCODE,
        "PhoneNumber": phone,
        "CallBackURL": CALLBACK_URL,
        "AccountReference": "Test Payment",
        "TransactionDesc": "Payment for product"
    }

    response = requests.post(stk_push_url, json=payload, headers=headers)
    print("Response Status Code:", response.status_code)
    print("Response Text:", response.text)
    return jsonify(response.json())





if __name__ == "__main__":
    app.run(debug=True)
