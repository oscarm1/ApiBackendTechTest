from decimal import Decimal
from .models import Customer, Loan
from .selectors import get_customer_by_external_id, calculate_total_debt
from django.db import transaction

def create_loan(data):
    external_id = data.get('external_id')
    customer_external_id = data.get('customer_external_id')
    amount = Decimal(data.get('amount'))
    contract_version = data.get('contract_version')

    customer = get_customer_by_external_id(customer_external_id)

    total_debt = calculate_total_debt(customer)

    if not customer:
        return None, {"error": "Customer not found"}

    if customer.status == 2:
        return None, {"error": "Customer is inactive"}
    
    if customer.score < total_debt + amount:
        return None, {"error": "Insificient client score"}

    outstanding = amount

    with transaction.atomic():
        loan = Loan.objects.create(external_id=external_id,customer_external_id=customer, amount=amount, outstanding=outstanding, contract_version= contract_version, status=2)
    
    return loan, None

def get_loans_by_customer(external_id):
    customer = get_customer_by_external_id(external_id)

    if not customer:
        return None

    loans = Loan.objects.filter(customer_external_id=customer)
    return loans
