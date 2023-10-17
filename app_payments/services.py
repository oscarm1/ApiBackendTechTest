from .models import Payment
from .selectors import get_customer_by_external_id, get_loan_by_external_id,calculate_total_debt, update_loan_status
from django.db import transaction
from decimal import Decimal

def create_payment(data):
    external_id = data.get('external_id')
    customer_external_id = data.get('customer_external_id')
    total_amount = Decimal(data.get('total_amount'))
    loan_external_id = data.get('loan_external_id')

    customer = get_customer_by_external_id(customer_external_id)

    if not customer:
        return None, {"error": "Customer not found"}

    if customer.status == 2:
        return None, {"error": "Customer is inactive"}

    print(loan_external_id)
    total_debt = calculate_total_debt(customer, loan_external_id)

    print(total_debt)
    print(total_amount)

    if total_amount > total_debt:
        error_message = f"Payment amount exceeds total debt, outstanding: {total_debt:.2f}"
        return None, {"error": error_message}
        #return None, {"error": "Payment amount exceeds total debt, outstanding: " + total_debt}

    #payments = Payment.objects.filter(loan_external_id=get_loan_by_external_id(loan_external_id))

    with transaction.atomic():
        payment = Payment.objects.create(external_id=external_id,customer_external_id=customer, loan_external_id=get_loan_by_external_id(loan_external_id), total_amount=total_amount, status=1)
    
    # Actualizar el estado de los préstamos y el monto pendiente
    update_loan_status(customer, total_amount, loan_external_id)

    return payment, None
