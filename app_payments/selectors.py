from .models import Customer, Loan, Payment

def calculate_total_debt(customer,loan_id):
    loans = Loan.objects.filter(customer_external_id=customer, status=2, external_id=loan_id)
    total_debt = sum(loan.outstanding for loan in loans)
    return total_debt

def get_customer_by_external_id(external_id):
    try:
        return Customer.objects.get(external_id=external_id)
    except Customer.DoesNotExist:
        return None

def get_loan_by_external_id(external_id):
    try:
        return Loan.objects.get(external_id=external_id)
    except Loan.DoesNotExist:
        return None
    
def update_loan_status(customer, payment_amount, loan_id):
    loans = Loan.objects.filter(external_id=loan_id, customer_external_id=customer)
    for loan in loans:
        if payment_amount >= loan.outstanding:
            loan.status = 4  # Cambiar el estado del préstamo a "paid"
            payment_amount -= loan.outstanding
            loan.outstanding = 0
            loan.save()  # Guardar los cambios en el modelo Loan
        else:
            update_outstanding(loan, payment_amount)  # Actualizar el monto pendiente
            payment_amount = 0
            loan.save()  # Guardar los cambios en el modelo Loan

def update_outstanding(loan, amount_paid):
    payments = Payment.objects.filter(loan_external_id=loan)
    total_paid = sum(payment.total_amount for payment in payments)
    loan.outstanding = max(loan.amount - total_paid, 0)  # Calcular y asignar monto pendiente
    loan.save()
