from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/callback", methods=["POST"])
def mpesa_callback():
    """Handle M-Pesa STK Push Callback"""
    data = request.get_json()

    if not data:
        return jsonify({"message": "No data received"}), 400

    # Extract transaction details
    stk_callback = data.get("Body", {}).get("stkCallback", {})
    result_code = stk_callback.get("ResultCode")
    result_desc = stk_callback.get("ResultDesc")
    checkout_request_id = stk_callback.get("CheckoutRequestID")

    # Check if the payment was successful
    if result_code == 0:
        metadata = stk_callback.get("CallbackMetadata", {}).get("Item", [])
        transaction_details = {item["Name"]: item.get("Value", None) for item in metadata}

        mpesa_receipt = transaction_details.get("MpesaReceiptNumber", "N/A")
        amount = transaction_details.get("Amount", 0)
        phone_number = transaction_details.get("PhoneNumber", "Unknown")

        print(f"✅ Payment Successful! Amount: {amount}, Receipt: {mpesa_receipt}, Phone: {phone_number}")

        return jsonify({
            "message": "Payment received successfully",
            "receipt": mpesa_receipt,
            "amount": amount,
            "phone": phone_number
        }), 200

    else:
        print(f"❌ Payment Failed! Reason: {result_desc}, CheckoutRequestID: {checkout_request_id}")
        return jsonify({
            "message": "Payment failed",
            "reason": result_desc
        }), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
