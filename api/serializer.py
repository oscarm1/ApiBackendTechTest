from rest_framework import serializers
from .models import Customer, Loan, Payment

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        exclude = ['created_at', 'updated_at']

class LoanSerializer(serializers.ModelSerializer):
    outstanding = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    class Meta:
        model = Loan
        exclude = ['created_at', 'updated_at', 'maximun_payment_date', 'taken_at']

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        exclude = ['created_at', 'updated_at', 'paid_at']
