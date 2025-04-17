from django.contrib import admin
from django.urls import path
from coin_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name="home"),
    path('wallet/buy/', views.buy_coins, name='buy_coins'),
    path('wallet/payment/verify/', views.verify_payment, name='verify_payment'),
]