import uuid
import requests
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Transaction, Wallet

# Define the coin packs for different price ranges
COIN_PACKS = [
    {"amount": 200, "label": "Basic"},
    {"amount": 500, "label": "Starter"},
    {"amount": 1000, "label": "Pro"},
    {"amount": 1500, "label": "Premium"},
    {"amount": 3000, "label": "Ultimate"},
]

# View to handle the coin purchase



def buy_coins(request):
    if request.method == "POST":
        amount = int(request.POST['amount'])
        user = request.user if request.user.is_authenticated else None
        coins = amount
        order_id = str(uuid.uuid4())  # Unique order ID for this transaction

        # Create a new transaction entry in the database
        transaction = Transaction.objects.create(
            user=user,
            amount=amount,
            coins=coins,
            order_id=order_id,
        )

        # Set up headers for the Cashfree API
        headers = {
            "Content-Type": "application/json",
            "x-api-version": "2022-01-01",
            "x-client-id": settings.CASHFREE_APP_ID,
            "x-client-secret": settings.CASHFREE_SECRET_KEY
        }

        # Create order data with fallback for anonymous users
        data = {
            "order_id": order_id,
            "order_amount": amount,
            "order_currency": "INR",
            "customer_details": {
                "customer_id": str(user.id) if user else str(uuid.uuid4()),
                "customer_email": user.email if user else "guest@example.com",
                "customer_phone": "9999999999"
            },
            "order_meta": {
                "return_url": f"http://127.0.0.1:8000/wallet/payment/verify/?order_id={order_id}"
            }
        }

        response = requests.post(f"{settings.CASHFREE_BASE_URL}/orders", json=data, headers=headers)

        if response.status_code == 200:
            payment_data = response.json()
            return redirect(payment_data['payment_link'])
        else:
            return render(request, 'coin_app/payment_failed.html')

    return render(request, 'coin_app/buy_coins.html', {'coin_packs': COIN_PACKS})

def verify_payment(request):
    order_id = request.GET.get("order_id")  # Get the order ID from the query string

    # Set up headers for the Cashfree API
    headers = {
        "Content-Type": "application/json",
        "x-api-version": "2022-01-01",
        "x-client-id": settings.CASHFREE_APP_ID,
        "x-client-secret": settings.CASHFREE_SECRET_KEY
    }

    # Request to Cashfree to verify the payment status
    res = requests.get(f"{settings.CASHFREE_BASE_URL}/orders/{order_id}", headers=headers)
    data = res.json()

    # Log the response data to check its structure
    print("Cashfree response data:", data)  # Log response for debugging

    # Find the transaction in the database using the order_id
    try:
        transaction = Transaction.objects.get(order_id=order_id)
    except Transaction.DoesNotExist:
        return render(request, "coin_app/payment_failed.html", {
            "message": "Transaction not found."
        })

    # Check if the order is paid
    if data.get("order_status") == "PAID":  # If the payment was successful
        # Check if the response has a valid 'payment_session_id' or 'order_id' for tracking
        payment_session_id = data.get("order_token", None)  # Use order_token if payment_session_id isn't present

        if payment_session_id:
            transaction.status = "SUCCESS"
            transaction.payment_id = payment_session_id  # Store the order_token as payment_id
            transaction.save()

            # Update the user's wallet with the purchased coins
            wallet, _ = Wallet.objects.get_or_create(user=transaction.user)
            wallet.balance += transaction.coins  # Add the purchased coins to wallet
            wallet.save()

            # Render the success page with the number of coins purchased
            return render(request, "index.html", {
                "coins": transaction.coins,
                "balance": wallet.balance
            })
        else:
            # Handle case where no valid payment ID or session ID is found
            return render(request, "coin_app/payment_failed.html", {
                "message": "Payment verification failed. No valid payment session ID found."
            })
    else:
        # If the payment failed, update the transaction status and show failure page
        transaction.status = "FAILED"
        transaction.save()
        return render(request, "coin_app/payment_failed.html", {
            "message": "Payment verification failed. Order status is not PAID."
        })
    
from django.shortcuts import render
from .models import Wallet

