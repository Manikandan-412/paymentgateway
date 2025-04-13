# wallet/models.py

from django.db import models
from django.contrib.auth.models import User

class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    balance = models.PositiveIntegerField(default=0)

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.PositiveIntegerField()
    coins = models.PositiveIntegerField()
    order_id = models.CharField(max_length=100, unique=True)
    payment_id = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=20, default='PENDING')  # PENDING, SUCCESS, FAILED
    created_at = models.DateTimeField(auto_now_add=True)

