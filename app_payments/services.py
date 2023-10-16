from .models import Customer, Loan, Payment
from .selectors import get_customer_by_external_id, get_loan_by_external_id,calculate_total_debt
from django.db import transaction

def create_payment(data):
    customer_id = data.get('customer_external_id')
    total_amount = data.get('total_amount')

    customer = get_customer_by_external_id(customer_id)

    if not customer:
        return None, {"error": "Customer not found"}

    if customer.status == 2:
        return None, {"error": "Customer is inactive"}

    total_debt = calculate_total_debt(customer)

    if total_amount > total_debt:
        return None, {"error": "Payment amount exceeds total debt"}

    payments = Payment.objects.filter(loan_external_id=get_loan_by_external_id(data['loan_external_id']))

    # Actualizar el estado de los préstamos y el monto pendiente
    update_loan_status(customer, payments, total_amount)

    with transaction.atomic():
        payment = Payment.objects.create(customer_external_id=customer, loan_external_id=get_loan_by_external_id(data['loan_external_id']), total_amount=total_amount, status=1)
    
    return payment, None
