import uuid
import requests
from django.conf import settings
from django.shortcuts import render, redirect
from .models import Transaction, Wallet

# Coin packs available for purchase
COIN_PACKS = [
    {"amount": 200, "label": "Basic"},
    {"amount": 500, "label": "Starter"},
    {"amount": 1000, "label": "Pro"},
    {"amount": 1500, "label": "Premium"},
    {"amount": 3000, "label": "Ultimate"},
]

# Home page – shows coin balance
def index(request):
    user = request.user if request.user.is_authenticated else None
    wallet, _ = Wallet.objects.get_or_create(user=user)
    return render(request, "index.html", {"balance": wallet.balance})

# Buy coins page – handles payment creation and redirection
def buy_coins(request):
    user = request.user if request.user.is_authenticated else None
    wallet, _ = Wallet.objects.get_or_create(user=user)

    if request.method == "POST":
        amount = int(request.POST['amount'])
        coins = amount
        order_id = str(uuid.uuid4())  # Unique order ID

        # Save transaction with status PENDING
        transaction = Transaction.objects.create(
            user=user,
            amount=amount,
            coins=coins,
            order_id=order_id,
        )

        # Prepare headers for Cashfree
        headers = {
            "Content-Type": "application/json",
            "x-api-version": "2022-01-01",
            "x-client-id": settings.CASHFREE_APP_ID,
            "x-client-secret": settings.CASHFREE_SECRET_KEY
        }

        # Create order data
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
            return render(request, 'coin_app/payment_failed.html', {"message": "Payment gateway error."})

    # Show buy_coins.html with current balance and coin packs
    return render(request, 'coin_app/buy_coins.html', {
        'coin_packs': COIN_PACKS,
        'balance': wallet.balance
    })

# Verify the payment after redirect from Cashfree
def verify_payment(request):
    order_id = request.GET.get("order_id")

    headers = {
        "Content-Type": "application/json",
        "x-api-version": "2022-01-01",
        "x-client-id": settings.CASHFREE_APP_ID,
        "x-client-secret": settings.CASHFREE_SECRET_KEY
    }

    # Check the payment status from Cashfree API
    res = requests.get(f"{settings.CASHFREE_BASE_URL}/orders/{order_id}", headers=headers)
    data = res.json()

    try:
        transaction = Transaction.objects.get(order_id=order_id)
    except Transaction.DoesNotExist:
        return render(request, "coin_app/payment_failed.html", {"message": "Transaction not found."})

    # Prevent re-adding coins on refresh
    if transaction.status == "SUCCESS":
        wallet, _ = Wallet.objects.get_or_create(user=transaction.user)
        return render(request, "coin_app/payment_success.html", {
            "coins": transaction.coins,
            "balance": wallet.balance
        })

    # If payment was successful
    if data.get("order_status") == "PAID":
        transaction.status = "SUCCESS"
        transaction.payment_id = data.get("order_token", "")
        transaction.save()

        wallet, _ = Wallet.objects.get_or_create(user=transaction.user)
        wallet.balance += transaction.coins
        wallet.save()

        return render(request, "coin_app/payment_success.html", {
            "coins": transaction.coins,
            "balance": wallet.balance
        })

    # Otherwise, mark as failed
    transaction.status = "FAILED"
    transaction.save()
    return render(request, "coin_app/payment_failed.html", {
        "message": "Payment was not successful."
    })
