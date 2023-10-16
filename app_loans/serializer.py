from rest_framework import serializers
from .models import Loan

class LoanSerializer(serializers.ModelSerializer):
    outstanding = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    class Meta:
        model = Loan
        exclude = ['created_at', 'updated_at', 'maximun_payment_date', 'taken_at','contract_version']
